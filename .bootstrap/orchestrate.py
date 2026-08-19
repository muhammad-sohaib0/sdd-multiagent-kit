#!/usr/bin/env python3
"""Bootstrap critique runner: sends a document to all six panel models and saves
their structured critiques per the seed schema. Scratch tooling for the bootstrap
run only — the shipped kit formalizes this in milestone 2."""
import argparse, json, os, re, ssl, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

UNAUTH_CTX = ssl.create_default_context()
UNAUTH_CTX.check_hostname = False
UNAUTH_CTX.verify_mode = ssl.CERT_NONE

DOC_PROMPT = """You are model {model_id}, one of six independent critics in a Spec-Driven Development loop, checking a milestone document for the SDD Multi-Agent Kit project.

Project brief (condensed history — this is in force for this document):
- The kit is an npm-distributed framework that brings Spec-Driven Development to CLI coding agents (Claude Code, Claude Desktop, OpenCode, Antigravity). The brief is described in output files PLAN.md / BOOTSTRAP.md.
- The kit's process: computational-thinking requirement scan, fixed constitution, dependency-ordered milestones, five-document sets (spec/plan/tasks/workflow/tests), a structural-completeness gate, a simplicity gate, a two-pass six-model critique loop, Clarify, a Stranger Test, and PHR/ADR history logging.
- Everything follows the constitution: Standalone-First, Observable Interfaces, Tests Before Implementation, Simplicity by Default, Framework Trust, Real-World Testing, Amendment Process.

You must review the DOCUMENT below and return ONLY a single JSON object — no prose outside it, no markdown fences — conforming EXACTLY to this schema (do not add or rename keys):

{json_schema}

Rubric dimensions (0-10 each): clarity, completeness, edge_case_coverage, internal_consistency, testability.

Rules for every issue you raise:
- {pass_rule}
- Each issue's "category" is ONE of: "objective" or "needs_clarify".
- Every "objective" issue must carry a suggested_fix.
- A "needs_clarify" issue is a genuine product/business decision that the drafter could not correctly infer; it does NOT need a suggested_fix, and it exists to be asked of the human in Clarify.

Verdict string is one of: "pass" or "needs_revision".

DOCUMENT follows immediately after the line "---DOCUMENT START---".
"""

JSON_SCHEMA = """{
  "model": "<your model id>",
  "document": "<document name>",
  "round": <int>,
  "pass": <int>,
  "overall_score": <int 0-10>,
  "scores": {
    "clarity": <int 0-10>,
    "completeness": <int 0-10>,
    "edge_case_coverage": <int 0-10>,
    "internal_consistency": <int 0-10>,
    "testability": <int 0-10>
  },
  "issues": [
    {
      "section": "<section id or name>",
      "category": "objective | needs_clarify",
      "problem": "<what is wrong>",
      "why_it_matters": "<impact on the build>",
      "suggested_fix": "<optional, required for objective>"
    }
  ],
  "verdict": "pass | needs_revision"
}"""

PASS1_RULE = ("You score ONLY the objective dimensions (clarity, structure, internal consistency, "
"presence of every required section). When you hit something genuinely subjective or a business "
"decision that an AI could not correctly infer, tag it category \"needs_clarify\" instead of "
"demanding a fix. Your job this round is to flag missing objective quality and compile the "
"needs_clarify list — NOT to demand perfection on every score.")
PASS2_RULE = ("This is a full-rigor pass after the human's Clarify answers have been folded in. "
"Score all five dimensions honestly against the brief and the constitution, and re-check that the "
"Clarify answers did not quietly break consistency elsewhere in the document.")

MODELS = [
    {"id": "nvidia/nemotron-3-ultra-550b-a55b", "provider": "nim"},
    {"id": "openai/gpt-oss-120b", "provider": "nim"},
    {"id": "deepseek-ai/deepseek-v4-flash-0731", "provider": "nim"},
    {"id": "z-ai/glm-5.2", "provider": "nim"},
    {"id": "gemini-3.6-flash", "provider": "google"},
    {"id": "minimax-m3:cloud", "provider": "ollama"},
]

def call_nim(model, key, prompt):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2}).encode()
    req = urllib.request.Request("https://integrate.api.nvidia.com/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300, context=UNAUTH_CTX) as r:
        d = json.loads(r.read().decode())
    return d["choices"][0]["message"]["content"]

def call_google(model, key, prompt):
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=body, headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300, context=UNAUTH_CTX) as r:
        d = json.loads(r.read().decode())
    return d["candidates"][0]["content"]["parts"][0]["text"]

def call_ollama(model, key, prompt):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}).encode()
    req = urllib.request.Request("https://ollama.com/api/chat", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300, context=UNAUTH_CTX) as r:
        d = json.loads(r.read().decode())
    return d["message"]["content"]

def extract_json(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.M)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
    return None

def validate_shape(o, model_id, doc, rnd, ps):
    if not isinstance(o, dict): return None, "not an object"
    scores = o.get("scores") or {}
    issues = o.get("issues")
    if not isinstance(issues, list): return None, "issues missing"
    try:
        flat = {**o, **scores}
        for k in ("overall_score", "clarity", "completeness", "edge_case_coverage", "internal_consistency", "testability"):
            if not isinstance(flat.get(k), int): return None, f"{k} not int"
        r = int(flat["overall_score"])
        if r < 10 and len(issues) == 0:
            return None, "low score with empty issues"
    except (TypeError, KeyError):
        return None, "bad numeric fields"
    o.setdefault("model", model_id); o.setdefault("document", doc); o.setdefault("round", rnd); o.setdefault("pass", ps)
    return o, None

def call(model, key, prompt):
    p = model["provider"]
    if p == "nim": return call_nim(model["id"], key, prompt)
    if p == "google": return call_google(model["id"], key, prompt)
    if p == "ollama": return call_ollama(model["id"], key, prompt)
    raise ValueError(f"unknown provider {p}")

def run(doc_path, doc_name, ps, rnd, out_dir, env):
    with open(doc_path) as f: content = f.read()

    def work(m, idx):
        prompt = DOC_PROMPT.format(model_id=m["id"], json_schema=JSON_SCHEMA, pass_rule=(PASS1_RULE if ps == 1 else PASS2_RULE)) + "\n---DOCUMENT START---\n" + content
        critiques, tried = [], 0
        ok = False
        while tried < 3 and not ok:
            tried += 1
            try:
                text = call(m, env[m["provider"]], prompt)
                o1 = extract_json(text)
                if o1 is not None:
                    obj, err = validate_shape(o1, m["id"], doc_name, rnd, ps)
                else:
                    obj, err = None, "parse"
                if obj is not None:
                    critiques.append(obj); ok = True
                    print(f"  [{idx}/6] {m['id']}: OK score={obj['overall_score']} verdict={obj['verdict']} issues={len(obj['issues'])}", flush=True)
                else:
                    print(f"  [{idx}/6] {m['id']}: round{tried} invalid ({err}) retry", flush=True)
                    if tried == 1:
                        continue
            except urllib.error.HTTPError as e:
                print(f"  [{idx}/6] {m['id']}: HTTP {e.code} attempt{tried}", flush=True)
                if e.code == 400: break
                if e.code == 429: time.sleep(10)
                elif e.code >= 500: time.sleep(8)
                elif tried == 3: time.sleep(8)
            except Exception as e:
                print(f"  [{idx}/6] {m['id']}: error attempt{tried}: {e.__class__.__name__}", flush=True)
                if tried < 3: time.sleep(8)
        return critiques[-1] if ok else None

    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(work, m, i + 1): m for i, m in enumerate(MODELS)}
        for f in as_completed(futs):
            r = f.result()
            if r is not None:
                results.append(r)
    combined = {"document": doc_name, "pass": ps, "round": rnd, "critics": results, "n_valid": len(results)}
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"pass{ps}-round{rnd}-{doc_name}.json")
    with open(path, "w") as f: json.dump(combined, f, indent=2)
    print(f"Wrote {path}: {len(results)}/6 valid critics", flush=True)
    return combined

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc"); ap.add_argument("--name"); ap.add_argument("--pass", dest="ps", type=int); ap.add_argument("--round", type=int, default=1); ap.add_argument("--out", default="outputs/critique-log")
    a = ap.parse_args()
    env = {p: os.environ.get(k) for p, k in
           (("nim", "NVIDIA_NIM_API_KEY"), ("google", "GOOGLE_AISTUDIO_API_KEY"), ("ollama", "OLLAMA_API_KEY"))}
    for k in list(env):
        if not env[k]: del env[k]
    run(a.doc, a.name, a.ps, a.round, a.out, env)