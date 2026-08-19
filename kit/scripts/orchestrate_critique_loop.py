#!/usr/bin/env python3
"""Run the SDD two-pass, multi-model critique loop against one milestone document.

One invocation = one pass over one document. Reads the critic panel from
kit/config/providers.yaml (no hard-coded model list). Calls all panel models
concurrently (staggered start to avoid free-tier rate-limit bursts), applies the
retry policy, enforces the response-schema validity rule, and writes one JSON
per round to outputs/critique-log/pass{1|2}-round{N}-{name}.json

Usage:
  orchestrate_critique_loop.py --doc <path> --name <id> --pass 1|2 --round N \
      [--out <dir>] [--round-cap N] [--timeout S] [--config <path>]

Exits 0 on success (round written), 2 on config/input errors, 3 when the round
produced no valid critics (escalation note on stderr).
"""
import argparse
import json
import os
import re
import sys
import threading
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import validate_critique
except ImportError:  # same-directory companion; checked before any run
    validate_critique = None

# ---------------------------------------------------------------- YAML subset
def _scalar(v):
    v = v.strip()
    if v in ("null", "~", ""):
        return None
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def load_yaml(text):
    """Return (data, error). Minimal YAML-subset reader for providers.yaml:
    nested maps ('key: value'), lists ('- item'), comments ('#'). Dependency-free."""
    try:
        lines = []
        for raw in text.splitlines():
            s = raw.split("#", 1)[0].rstrip()
            if not s.strip():
                continue
            lines.append((len(raw) - len(raw.lstrip(" ")), s.strip()))
        data, _ = _block(lines, 0, 0)
        return data, None
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def _block(items, i, indent):
    """Parse items[i:] at the given indent into a dict or list. Returns (node, next_i)."""
    node = {}
    made_list = False
    while i < len(items):
        ind, text = items[i]
        if ind < indent:
            break
        if text.startswith("- "):
            if not made_list:
                node = []
                made_list = True
            el, i = _list_element(items, i)
            node.append(el)
            continue
        if ":" in text:
            key, _, rest = text.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == "":
                if i + 1 < len(items) and items[i + 1][0] > ind:
                    child, ni = _block(items, i + 1, items[i + 1][0])
                    node[key] = child
                    i = ni
                else:
                    node[key] = None
                    i += 1
            else:
                node[key] = _scalar(rest)
                i += 1
        else:
            i += 1
    return node, i


def _list_element(items, i):
    """Parse a '- ' list element. Returns (element_dict_or_scalar, next_i).
    A map element is indicated by ': ' (colon+space) or a trailing ':' (nested
    block); otherwise the body is a scalar even if it contains ':' (e.g. a
    model id like 'minimax-m3:cloud')."""
    ind, text = items[i]
    body = text[2:].strip()
    d = {}
    j = i + 1
    is_map = (": " in body) or body.endswith(":")
    if is_map:
        key, _, rest = body.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "" and j < len(items) and items[j][0] > ind:
            child, nj = _block(items, j, items[j][0])
            d[key] = child
            j = nj
        else:
            d[key] = _scalar(rest)
    else:
        if j < len(items) and items[j][0] > ind:
            _, nj = _block(items, j, items[j][0])
            j = nj
        return _scalar(body), j
    while j < len(items) and items[j][0] > ind:
        jind, jtext = items[j]
        if ":" in jtext:
            k, _, v = jtext.partition(":")
            v = v.strip()
            if v == "" and j + 1 < len(items) and items[j + 1][0] > jind:
                child, nj = _block(items, j + 1, items[j + 1][0])
                d[k] = child
                j = nj
            else:
                d[k] = _scalar(v)
                j += 1
        else:
            j += 1
    return d, j


# ------------------------------------------------------------- provider calls
UNAUTH_CTX = None
try:
    import ssl
    UNAUTH_CTX = ssl._create_unverified_context()
except Exception:  # noqa: BLE001
    pass

JSON_SCHEMA = """{
  "model": "<model-id>", "document": "<doc-name>", "round": <round>, "pass": <1|2>,
  "overall_score": 0-10,
  "scores": {"clarity":0-10,"completeness":0-10,"edge_case_coverage":0-10,
             "internal_consistency":0-10,"testability":0-10},
  "issues": [{"section":"","category":"objective|needs_clarify",
              "problem":"","why_it_matters":"","suggested_fix":""}],
  "verdict": "pass|needs_revision"
}"""

PASS1_RULE = ("Pass 1 (light): score only the objective dimensions — clarity, "
              "completeness, edge_case_coverage, internal_consistency (all checkable "
              "against the document alone); testability is subjective (it needs a "
              "runtime) and is out of Pass-1 scope — the schema still requires the "
              "key, so emit testability as 0 (not assessed in this pass). Tag "
              "anything that is a genuine "
              "business/subjective decision with category \"needs_clarify\". Stop once "
              "every objective issue is resolved and the needs_clarify list is "
              "compiled.")
PASS2_RULE = ("Pass 2 (full rigor): score every dimension at full strictness. "
              "Be alert for internal inconsistencies introduced by recent edits. "
              "You may still tag genuinely new business/subjective decisions with "
              "category \"needs_clarify\" (the category is pass-independent). "
              "Return a perfect score only when the document requires no revision.")

DOC_PROMPT = """You are critic {model_id} in a multi-model SDD critique loop. Review the document
below and return ONLY a JSON object matching exactly this schema:
{json_schema}
{pass_rule}
Be strict, specific, and unflattering. Never score below 10 with an empty issues list.
---DOCUMENT START---
"""


def _post(payload, url, headers, timeout):
    """POST and return the response text, enforcing a hard wall-clock deadline.

    Socket-level timeouts alone do not bound a call: some free-tier endpoints
    drip bytes slowly enough that every socket read restarts the timer, hanging
    the round indefinitely. So the request runs on a daemon thread and the
    caller abandons it at the deadline, whatever the socket thinks."""
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    result = {}

    def _do():
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=UNAUTH_CTX) as r:
                result["text"] = r.read().decode()
        except BaseException as e:  # noqa: BLE001
            result["err"] = e

    t = threading.Thread(target=_do, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        raise TimeoutError(f"provider call exceeded {timeout}s (hard deadline)")
    if "err" in result:
        raise result["err"]
    return result["text"]


def call_nim(model_id, key, prompt, timeout):
    url = f"https://integrate.api.nvidia.com/v1/chat/completions"
    payload = {"model": model_id, "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.2, "max_tokens": 8000}
    text = _post(payload, url, {"Authorization": f"Bearer {key}",
                                "Content-Type": "application/json"}, timeout)
    return json.loads(text)["choices"][0]["message"]["content"]


def call_google(model_id, key, prompt, timeout):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8000}}
    text = _post(payload, f"{url}?key={key}", {"Content-Type": "application/json"}, timeout)
    return json.loads(text)["candidates"][0]["content"]["parts"][0]["text"]


def call_ollama(model_id, key, prompt, timeout):
    url = "https://ollama.com/api/chat"
    payload = {"model": model_id, "messages": [{"role": "user", "content": prompt}],
               "stream": False, "options": {"temperature": 0.2, "num_predict": 12000}}
    text = _post(payload, url, {"Authorization": f"Bearer {key}",
                                "Content-Type": "application/json"}, timeout)
    return json.loads(text)["message"]["content"]


def call(model, key, prompt, timeout):
    eff = model.get("timeout") or timeout
    p = model["provider"]
    if p == "nvidia-nim":
        return call_nim(model["model"], key, prompt, eff)
    if p == "google-ai-studio":
        return call_google(model["model"], key, prompt, eff)
    if p == "ollama-cloud":
        return call_ollama(model["model"], key, prompt, eff)
    raise ValueError(f"unknown provider {p}")


# --------------------------------------------------------------- validation
def _balanced_candidates(text):
    """Yield substrings starting at each '{' and closing at the first
    depth-balanced '}', in order. String literals are honored so braces
    inside quoted text never affect depth."""
    start = -1
    depth = 0
    in_str = False
    esc = False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start >= 0:
                yield text[start:i + 1]
                start = -1


def _repair_truncated(text, validate):
    """Best-effort repair of a response truncated mid-JSON (free-tier output
    caps). Tries every '{' as a candidate JSON start, in text order, closes an
    unterminated string, and appends the minimal closing brackets; only the
    first candidate that passes the full validity check wins, so a bad repair
    never counts against the critic."""
    starts = [i for i, ch in enumerate(text) if ch == "{"]
    for start in starts:
        s = text[start:]
        stack = []
        in_str = False
        esc = False
        for ch in s:
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch in "{[":
                stack.append(ch)
            elif ch in "}]" and stack:
                stack.pop()
        out = s + ('"' if in_str else "")
        for ch in reversed(stack):
            out += "}" if ch == "{" else "]"
        try:
            o = json.loads(out)
        except ValueError:
            continue
        o, err = validate(o)
        if err is None:
            return o
    return None


def extract_json(text, validate):
    """Extract the JSON object from a model response. Tolerant of markdown
    fences (anywhere, not just at the start), surrounding prose — including
    prose that itself contains braces — trailing commas, and output-cap
    truncation (all common free-tier failure modes). Candidates are tried in
    text order and only the first that passes the full validity check wins, so
    a bad repair never counts. Returns (object, None) or (None, reason)."""
    if not text:
        return None, "no response text"
    text = text.strip()
    candidates = []
    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.S)
    if m:
        candidates.append(m.group(1))
    candidates.append(text)
    cleaned = [re.sub(r",(\s*[}\]])", r"\1", c) for c in candidates]
    last_err = None
    for c in cleaned:
        for sub in _balanced_candidates(c):
            try:
                o = json.loads(sub)
            except ValueError:
                continue
            o, err = validate(o)
            if err is None:
                return o, None
            last_err = err
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            o = json.loads(re.sub(r",(\s*[}\]])", r"\1", m.group(0)))
            o, err = validate(o)
            if err is None:
                return o, None
            last_err = err
        except ValueError:
            pass
    for c in cleaned:
        r = _repair_truncated(c, validate)
        if r is not None:
            return r, None
    return None, last_err or "no parseable JSON"


def _as_int(v):
    """Coerce a score to int; accept int, float, and numeric strings."""
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(round(v))
    if isinstance(v, str):
        try:
            return int(round(float(v)))
        except ValueError:
            return None
    return None


def validate_shape(o, ps=None):
    """Full validity check for one critic response.

    The response must parse into the PLAN.md section-4.3 schema shape — all
    required fields present with the required types (delegated to the shape
    authority validate_critique.validate_single, so the loop can never write a
    file its own validator rejects) — and satisfy the semantic noise rule
    (overall_score < 10 with zero issues is invalid). Numeric scores are
    coerced to int first, so float emissions from critics still count.

    When ps == 1, testability is normalized to 0 ("not assessed in this pass",
    PLAN.md section 4.2). Free-tier critics routinely ignore that instruction
    and score the dimension anyway, so it is corrected here rather than treated
    as invalid: the rule is a scoping convention, not a correctness test, and
    rejecting an otherwise-good critique over it would discard real signal.
    Nothing in the section-4.4 stopping conditions reads testability, so this
    changes no decision — it only stops the log from claiming a runtime was
    judged when none existed.
    Returns (normalized_object, None) or (None, reason)."""
    if not isinstance(o, dict):
        return None, "not object"
    if not isinstance(o.get("issues"), list):
        return None, "issues missing"
    try:
        sc = o.get("scores") or {}
        flat = dict(o)
        flat.update(sc)
        for k in ("overall_score", "clarity", "completeness", "edge_case_coverage",
                  "internal_consistency", "testability"):
            v = _as_int(flat.get(k))
            if v is None:
                return None, f"{k} not numeric"
            flat[k] = v
        if ps == 1:
            flat["testability"] = 0
        o["overall_score"] = flat["overall_score"]
        o.setdefault("scores", {})
        for k in ("clarity", "completeness", "edge_case_coverage",
                  "internal_consistency", "testability"):
            o["scores"][k] = flat[k]
    except (TypeError, KeyError):
        return None, "bad numeric fields"
    if validate_critique is None:
        return None, "validate_critique.py unavailable"
    problems = validate_critique.validate_single(o, 0)
    if problems:
        return None, problems[0].rsplit(": ", 1)[-1]
    if o["overall_score"] < 10 and len(o["issues"]) == 0:
        return None, "low score with empty issues"
    return o, None


# --------------------------------------------------------------------- loop
def run(doc_path, doc_name, ps, rnd, out_dir, env, timeout, round_cap, config_path):
    if not doc_name:
        print("error: --name must not be empty", file=sys.stderr)
        return 2
    if "/" in doc_name or "\\" in doc_name:
        print(f"error: --name must be a plain document id (no path separators): {doc_name}", file=sys.stderr)
        return 2
    if not os.path.exists(doc_path):
        print(f"error: document not found: {doc_path}", file=sys.stderr)
        return 2
    try:
        with open(doc_path) as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"error: document is not valid UTF-8 text: {doc_path}", file=sys.stderr)
        return 2
    if not content.strip():
        print(f"error: document is empty: {doc_path}", file=sys.stderr)
        return 2
    if not os.path.exists(config_path):
        print(f"error: config not found: {config_path}", file=sys.stderr)
        return 2
    cfg, err = load_yaml(open(config_path).read())
    if err or not cfg:
        print(f"error: cannot parse config: {err}", file=sys.stderr)
        return 2
    providers_list = cfg.get("providers") or []
    if not isinstance(providers_list, list) or not providers_list:
        print("error: config has no providers list", file=sys.stderr)
        return 2
    providers = {}
    for p in providers_list:
        if not isinstance(p, dict) or not p.get("id"):
            print("error: malformed provider entry in config", file=sys.stderr)
            return 2
        providers[p["id"]] = p
    # Keys are read at runtime from the process environment via each provider's
    # key_env field — names only travel in config/code, never values (AC-6).
    env_map = {}
    for pid, p in providers.items():
        kn = p.get("key_env")
        if not kn:
            print(f"error: provider '{pid}' has no key_env", file=sys.stderr)
            return 2
        env_map[pid] = env.get(kn)
    slots = cfg.get("critic_slots") or []
    if not isinstance(slots, list) or not slots:
        print("error: config has no critic_slots list", file=sys.stderr)
        return 2
    models = []
    for s in slots:
        if not isinstance(s, dict) or not s.get("model") or not s.get("provider"):
            print("error: malformed critic_slot entry", file=sys.stderr)
            return 2
        p = providers.get(s["provider"])
        if p is None:
            print(f"error: unknown provider '{s['provider']}' for slot {s['model']}", file=sys.stderr)
            return 2
        if not isinstance(p.get("models"), list):
            print(f"error: provider {s['provider']} has no models list", file=sys.stderr)
            return 2
        # Accept both schema forms for a model entry: the §4.3 map form
        # ('- id: <model>') and the plain-scalar form; both are normalized to
        # the model id string for the slot membership check.
        model_ids = []
        for m in p["models"]:
            if isinstance(m, str):
                model_ids.append(m)
            elif isinstance(m, dict) and isinstance(m.get("id"), str):
                model_ids.append(m["id"])
        if s["model"] not in model_ids:
            print(f"error: slot model {s['model']} not in provider {s['provider']}", file=sys.stderr)
            return 2
        if not env_map.get(s["provider"]):
            print(f"error: no env key for provider {s['provider']}", file=sys.stderr)
            return 2
        t = s.get("timeout")
        if t is not None and (not isinstance(t, (int, float)) or isinstance(t, bool) or t <= 0):
            print(f"error: slot {s['model']}: timeout must be a positive number", file=sys.stderr)
            return 2
        models.append(s)

    def work(m, idx):
        # Staggered start: free-tier rate limits are per-key and per-minute, so
        # firing every model at t=0 guarantees a 429 burst. Offset each critic's
        # first call (4s apart) so concurrent starts never align.
        time.sleep((idx - 1) * 4)
        prompt = DOC_PROMPT.format(model_id=m["model"], json_schema=JSON_SCHEMA,
                                   pass_rule=(PASS1_RULE if ps == 1 else PASS2_RULE)) + content
        invalid_tries = 0
        transport_tries = 0
        last_text = None
        while invalid_tries < 2 and transport_tries < 5:
            try:
                text = call(m, env_map[m["provider"]], prompt, timeout)
                last_text = text
                obj, err = extract_json(text, lambda o: validate_shape(o, ps))
                if obj is not None:
                    print(f"  [{idx}/{len(models)}] {m['model']}: OK score={obj['overall_score']} "
                          f"verdict={obj['verdict']} issues={len(obj['issues'])}", flush=True)
                    return obj
                invalid_tries += 1
                print(f"  [{idx}/{len(models)}] {m['model']}: invalid attempt{invalid_tries} ({err})", flush=True)
                if invalid_tries == 1:
                    continue
                break  # invalid twice -> give up this round
            except urllib.error.HTTPError as e:
                print(f"  [{idx}/{len(models)}] {m['model']}: HTTP {e.code} attempt{transport_tries + 1}", flush=True)
                if 400 <= e.code < 500 and e.code != 429:
                    break  # deterministic client error (auth, bad request, not found)
                transport_tries += 1
                if transport_tries >= 5:
                    break
                if e.code == 429:
                    # Adaptive: a 429 is a time-based quota; give each retry a
                    # progressively longer window to clear it.
                    time.sleep(30 * transport_tries)
                else:
                    time.sleep(8 * transport_tries)
            except Exception as e:  # noqa: BLE001
                print(f"  [{idx}/{len(models)}] {m['model']}: error attempt{transport_tries + 1}: "
                      f"{e.__class__.__name__}", flush=True)
                transport_tries += 1
                if transport_tries >= 5:
                    break
                time.sleep(8 * transport_tries)
        if last_text:
            snippet = " ".join(last_text.strip().split())[:300]
            print(f"    last raw text: {snippet}", flush=True)
        return None

    results = []
    with ThreadPoolExecutor(max_workers=len(models)) as ex:
        futs = {ex.submit(work, m, i + 1): i + 1 for i, m in enumerate(models)}
        for f in as_completed(futs):
            r = f.result()
            if r is not None:
                results.append((futs[f], r))
    results.sort(key=lambda t: t[0])
    combined = {"document": doc_name, "pass": ps, "round": rnd,
                "critics": [r for _, r in results], "n_valid": len(results)}
    # Self-check via the shape authority before anything is written: the loop
    # must never emit a file its own validator would reject (plan section 2).
    if validate_critique is None:
        print("error: validate_critique.py not importable (required self-check)", file=sys.stderr)
        return 2
    problems = validate_critique.validate_envelope(combined)
    if problems:
        print("error: self-check failed; not writing output: " + "; ".join(problems), file=sys.stderr)
        return 2
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        print(f"error: cannot create output directory {out_dir}: {e}", file=sys.stderr)
        return 2
    path = os.path.join(out_dir, f"pass{ps}-round{rnd}-{doc_name}.json")
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w") as f:
            json.dump(combined, f, indent=2)
        os.replace(tmp_path, path)
    except OSError as e:
        print(f"error: cannot write output {path}: {e}", file=sys.stderr)
        return 2
    print(f"Wrote {path}: {len(results)}/{len(models)} valid critics")
    if len(results) == 0:
        print("escalation: round produced no valid critics", file=sys.stderr)
        return 3
    return 0


def main():
    ap = argparse.ArgumentParser(description="SDD critique-loop orchestrator")
    ap.add_argument("--doc", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--pass", dest="ps", type=int, choices=[1, 2], required=True)
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--out", default="outputs/critique-log")
    ap.add_argument("--round-cap", type=int, default=25)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--config", default="kit/config/providers.yaml")
    a = ap.parse_args()
    if a.round < 1:
        print("error: --round must be a positive integer", file=sys.stderr)
        return 2
    if a.round_cap < 0:
        print("error: --round-cap must be a positive integer or 0", file=sys.stderr)
        return 2
    if a.timeout <= 0:
        print("error: --timeout must be a positive number of seconds", file=sys.stderr)
        return 2
    return run(a.doc, a.name, a.ps, a.round, a.out, os.environ,
               a.timeout, a.round_cap, a.config)


if __name__ == "__main__":
    sys.exit(main())