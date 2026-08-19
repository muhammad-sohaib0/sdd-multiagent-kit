#!/usr/bin/env python3
"""M2 verification suite — NT1..NT9 per outputs/milestones/milestone_2/tests_milestone_2.md.

Run:  python3 verify_milestone_2.py
Exit 0 = all nodes pass, 1 = any failure. Network is mocked; the real end-to-end
round (walkthrough section 3) is run separately with live provider keys.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KIT_SCRIPTS = os.path.join(REPO, "kit", "scripts")
sys.path.insert(0, KIT_SCRIPTS)
import orchestrate_critique_loop as oc  # noqa: E402
import validate_critique as vc  # noqa: E402

REAL_CONFIG = os.path.join(REPO, "kit", "config", "providers.yaml")
REAL_ENV = {"NVIDIA_NIM_API_KEY": "k", "GOOGLE_AISTUDIO_API_KEY": "k", "OLLAMA_API_KEY": "k"}
REAL_SLOTS = [
    "nvidia/nemotron-3-ultra-550b-a55b", "openai/gpt-oss-120b", "z-ai/glm-5.2",
    "mistralai/mistral-nemotron", "meta/muse-glimmer-30b", "gemini-3.6-flash",
    "minimax-m3:cloud",
]
REAL_PROVIDERS = {"nvidia-nim", "google-ai-studio", "ollama-cloud"}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"Bearer [A-Za-z0-9._-]{20,}"),
]

ARTIFACTS = [
    os.path.join(KIT_SCRIPTS, "orchestrate_critique_loop.py"),
    os.path.join(KIT_SCRIPTS, "validate_critique.py"),
    os.path.join(REPO, "kit", "skills", "critique-loop", "SKILL.md"),
]


def make_critique(model, score=8, issues=None, verdict="needs_revision", doc="d", rnd=1, ps=1):
    return {
        "model": model, "document": doc, "round": rnd, "pass": ps,
        "overall_score": score,
        "scores": {"clarity": score, "completeness": score,
                   "edge_case_coverage": score, "internal_consistency": score,
                   "testability": score},
        "issues": issues if issues is not None else
                  [{"section": "s", "category": "objective", "problem": "p"}],
        "verdict": verdict,
    }


def single_slot_config(key_env="TEST_KEY"):
    """A 1-slot providers.yaml for deterministic retry/backoff tests."""
    return {
        "version": 1,
        "providers": [{"id": "test-pro", "key_env": key_env, "tier": "free",
                       "models": ["test-model-1"]}],
        "critic_slots": [{"model": "test-model-1", "provider": "test-pro"}],
    }


def model_id(entry):
    """Normalize a providers.yaml `models:` entry to its model-id string.

    The §4.3 schema form is a map (`- id: <model>`), which is what the shipped
    config uses; the orchestrator also accepts a plain scalar (`- <model>`).
    Both forms reach here, so tests compare ids rather than raw entries."""
    if isinstance(entry, dict):
        return entry.get("id")
    return entry


def write_temp_config(data):
    """Serialize the small config dict as YAML text (the engine's own reader
    parses YAML, not JSON) and return the temp file path.

    A `models:` entry is re-emitted in the form it came in — map entries as
    `- id: <model>` (the §4.3 schema form) and scalars as `- <model>` — so a
    config read from the shipped file round-trips unchanged, and both accepted
    forms stay covered by the suite."""
    fd, path = tempfile.mkstemp(suffix=".yaml")
    with os.fdopen(fd, "w") as f:
        f.write("version: 1\n")
        f.write("providers:\n")
        for p in data["providers"]:
            f.write(f"  - id: {p['id']}\n")
            f.write(f"    key_env: {p['key_env']}\n")
            f.write(f"    tier: {p.get('tier', 'free')}\n")
            f.write("    models:\n")
            for m in p["models"]:
                if isinstance(m, dict):
                    f.write(f"      - id: {m['id']}\n")
                else:
                    f.write(f"      - {m}\n")
        f.write("critic_slots:\n")
        for s in data["critic_slots"]:
            f.write(f"  - model: {s['model']}\n")
            f.write(f"    provider: {s['provider']}\n")
            if "timeout" in s:
                f.write(f"    timeout: {s['timeout']}\n")
    return path


def run_round(cfg_path, doc_name, ps=1, rnd=1, round_cap=25, timeout=30,
              env=None, out_dir=None, extra_models=None):
    """Drive oc.run() with a fresh temp doc and an out dir; returns (rc, out_dir, sleeps, calls)."""
    doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
    doc.write("# Test document\n\nShort excerpt for mocked rounds.\n")
    doc.close()
    if out_dir is None:
        out_dir = tempfile.mkdtemp(prefix="m2out-")
    env = env or REAL_ENV
    sleeps, calls = [], {}
    real_sleep = time.sleep

    def fake_sleep(s):
        sleeps.append(s)

    def fake_call(m, key, prompt, timeout_s):
        calls[m["model"]] = calls.get(m["model"], 0) + 1
        return prompt_critique(m)

    def prompt_critique(m):
        return json.dumps(make_critique(m["model"], doc=doc_name, rnd=rnd, ps=ps))

    with mock.patch("time.sleep", side_effect=fake_sleep), \
         mock.patch.object(oc, "call", side_effect=fake_call):
        rc = oc.run(doc.name, doc_name, ps, rnd, out_dir, env,
                    timeout, round_cap, cfg_path)
    os.unlink(doc.name)
    return rc, out_dir, sleeps, calls


class NT1ConfigDriven(unittest.TestCase):
    """NT1 — R0 config-driven panel (AC-2)."""

    def test_panel_read_from_config(self):
        cfg, err = oc.load_yaml(open(REAL_CONFIG).read())
        self.assertIsNone(err)
        slots = cfg["critic_slots"]
        self.assertEqual([s["model"] for s in slots], REAL_SLOTS)
        self.assertEqual([s["provider"] for s in slots], ["nvidia-nim"] * 5 + ["google-ai-studio", "ollama-cloud"])
        models = {p["id"]: [model_id(m) for m in p["models"]] for p in cfg["providers"]}
        for s in slots:
            self.assertIn(s["model"], models[s["provider"]])
            self.assertIn("key_env", {p["id"]: p for p in cfg["providers"]}[s["provider"]])
        self.assertEqual(len({s["model"] for s in slots}), 7)

    def test_no_hardcoded_models(self):
        def code_only(src):
            # Comments and docstrings may mention example ids (e.g. the YAML
            # reader's comment); only executable code must be model-free.
            import io
            import tokenize
            parts = []
            for t in tokenize.generate_tokens(io.StringIO(src).readline):
                if t.type not in (tokenize.COMMENT, tokenize.STRING):
                    parts.append(t.string)
            return " ".join(parts)
        src = code_only(open(os.path.join(KIT_SCRIPTS, "orchestrate_critique_loop.py")).read())
        for m in REAL_SLOTS:
            self.assertNotIn(m, src, f"model {m} hard-coded in orchestrator")
        srcv = code_only(open(os.path.join(KIT_SCRIPTS, "validate_critique.py")).read())
        for m in REAL_SLOTS:
            self.assertNotIn(m, srcv, f"model {m} hard-coded in validator")

    def test_model_added_via_config_only(self):
        # US-4: extend the panel in config; the engine picks it up with zero code change.
        cfg, _ = oc.load_yaml(open(REAL_CONFIG).read())
        cfg["providers"][0]["models"].append("brand-new-model-x")
        cfg["critic_slots"].append({"model": "brand-new-model-x", "provider": "nvidia-nim"})
        p = write_temp_config(cfg)
        rc, out_dir, sleeps, calls = run_round(p, "nt1us4")
        self.assertEqual(rc, 0)
        self.assertEqual(len(calls), 8, "8th config-added model must be called")
        self.assertIn("brand-new-model-x", calls)
        data = json.load(open(os.path.join(out_dir, "pass1-round1-nt1us4.json")))
        self.assertEqual([c["model"] for c in data["critics"]],
                         REAL_SLOTS + ["brand-new-model-x"], "critique order = critic_slots order")
        os.unlink(p)

    def test_both_model_entry_schema_forms_accepted(self):
        # The §4.3 schema form is the map (`- id: X`) the shipped config uses;
        # the loader also accepts a plain scalar (`- X`). Both must resolve for
        # the slot-membership check, so neither form can drift out of coverage.
        for label, entries in (("map", [{"id": "m-a"}, {"id": "m-b"}]),
                               ("scalar", ["m-a", "m-b"]),
                               ("mixed", [{"id": "m-a"}, "m-b"])):
            cfg = {
                "version": 1,
                "providers": [{"id": "p1", "key_env": "NVIDIA_NIM_API_KEY",
                               "tier": "free", "models": entries}],
                "critic_slots": [{"model": "m-a", "provider": "p1"},
                                 {"model": "m-b", "provider": "p1"}],
            }
            p = write_temp_config(cfg)
            rc, out_dir, _sleeps, calls = run_round(p, f"nt1form{label}")
            self.assertEqual(rc, 0, f"{label} form must load")
            self.assertEqual(sorted(calls), ["m-a", "m-b"], f"{label} form must call both slots")
            os.unlink(p)

    def test_shipped_config_uses_the_schema_map_form(self):
        # Pins the shipped config to the §4.3 map form so a silent switch to
        # bare scalars (or a helper that emits Python reprs) is caught here
        # rather than surfacing as an unexplained exit-2 later.
        cfg, err = oc.load_yaml(open(REAL_CONFIG).read())
        self.assertIsNone(err)
        for p in cfg["providers"]:
            for m in p["models"]:
                self.assertIsInstance(m, dict, "shipped models must use '- id: <model>'")
                self.assertIsInstance(m.get("id"), str)

    def test_config_round_trips_through_the_suite_helper(self):
        # write_temp_config must re-emit what load_yaml read; a lossy helper
        # was the original cause of this suite drifting from the shipped config.
        cfg, _ = oc.load_yaml(open(REAL_CONFIG).read())
        p = write_temp_config(cfg)
        again, err = oc.load_yaml(open(p).read())
        os.unlink(p)
        self.assertIsNone(err)
        self.assertEqual([model_id(m) for pr in again["providers"] for m in pr["models"]],
                         [model_id(m) for pr in cfg["providers"] for m in pr["models"]])
        self.assertEqual([s["model"] for s in again["critic_slots"]], REAL_SLOTS)

    def test_critics_ordered_by_slot_not_completion(self):
        # Deterministic slot order even when completion order differs.
        real_sleep = time.sleep
        delay = {"nvidia/nemotron-3-ultra-550b-a55b": 0.15, "minimax-m3:cloud": 0.0}
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        out_dir = tempfile.mkdtemp(prefix="m2ord-")
        with mock.patch("time.sleep", side_effect=lambda s: None):
            def fake_call(m, key, prompt, timeout_s):
                d = delay.get(m["model"], 0.05)
                real_sleep(d)
                return json.dumps(make_critique(m["model"], doc="ord", rnd=1, ps=1))
            with mock.patch.object(oc, "call", side_effect=fake_call):
                rc = oc.run(doc.name, "ord", 1, 1, out_dir, REAL_ENV, 30, 25, REAL_CONFIG)
        os.unlink(doc.name)
        self.assertEqual(rc, 0)
        data = json.load(open(os.path.join(out_dir, "pass1-round1-ord.json")))
        self.assertEqual([c["model"] for c in data["critics"]], REAL_SLOTS)


class NT2ValiditySplit(unittest.TestCase):
    """NT2 — R1/R2 validity rule; shape in the validator, semantic rule in the orchestrator."""

    def _with_testability(self, ps, emitted):
        """A valid critique whose four objective dims are 7 and testability is `emitted`."""
        c = make_critique("m", score=7, ps=ps)
        c["scores"]["testability"] = emitted
        return c

    def test_pass1_normalizes_testability_to_zero(self):
        # PLAN.md §4.2: testability is out of Pass-1 scope, so a Pass-1 response
        # carries testability 0 ("not assessed in this pass"). Free-tier critics
        # ignore the instruction routinely, so the engine normalizes rather than
        # rejecting — losing a whole critique over a scoping convention would
        # trade real signal for tidiness.
        for emitted in (7, 9, 10, 0):
            o, err = oc.validate_shape(self._with_testability(1, emitted), 1)
            self.assertIsNone(err, f"testability {emitted} must not invalidate a Pass-1 critique")
            self.assertEqual(o["scores"]["testability"], 0,
                             f"Pass-1 testability {emitted} must normalize to 0")
            # the other four dimensions and the holistic score are untouched
            self.assertEqual(o["scores"]["clarity"], 7)
            self.assertEqual(o["scores"]["internal_consistency"], 7)
            self.assertEqual(o["overall_score"], 7)

    def test_pass2_preserves_testability(self):
        # Pass 2 scores every dimension at full strictness — no normalization.
        for emitted in (7, 0, 10):
            o, err = oc.validate_shape(self._with_testability(2, emitted), 2)
            self.assertIsNone(err)
            self.assertEqual(o["scores"]["testability"], emitted,
                             "Pass 2 must not rewrite testability")

    def test_pass1_written_log_carries_zero_testability(self):
        # End-to-end: a mocked Pass-1 round whose critics all score testability
        # 8 must land on disk as 0, and the file must still pass the validator.
        rc, out_dir, _s, _c = run_round(REAL_CONFIG, "nt2norm", ps=1)
        self.assertEqual(rc, 0)
        data = json.load(open(os.path.join(out_dir, "pass1-round1-nt2norm.json")))
        self.assertTrue(data["critics"], "round must have produced critics")
        for c in data["critics"]:
            self.assertEqual(c["scores"]["testability"], 0,
                             f"{c['model']} wrote a non-zero Pass-1 testability")
        self.assertEqual(vc.validate_envelope(data), [])

    def _run_validator(self, path, stdin=False):
        cmd = [sys.executable, os.path.join(KIT_SCRIPTS, "validate_critique.py")]
        if not stdin:
            cmd += ["--file", path]
        with open(path, "rb") as inp:
            return subprocess.run(cmd, stdin=inp, capture_output=True, text=True)

    def test_valid_file_exit_0(self):
        env = {"document": "d", "pass": 1, "round": 1,
               "critics": [make_critique("m")], "n_valid": 1}
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(env, f)
        r = self._run_validator(path)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("invalid:", r.stdout)
        r2 = self._run_validator(path, stdin=True)
        self.assertEqual(r2.returncode, 0)
        os.unlink(path)

    def test_malformed_exit_1_named_field(self):
        def env_with(crit):
            return {"document": "d", "pass": 1, "round": 1, "critics": [crit], "n_valid": 1}

        def write(crit):
            fd, path = tempfile.mkstemp(suffix=".json")
            with os.fdopen(fd, "w") as f:
                json.dump(env_with(crit), f)
            return path

        # missing required field -> exit 1, field named
        path = write({k: v for k, v in make_critique("m").items() if k != "verdict"})
        r = self._run_validator(path)
        self.assertEqual(r.returncode, 1, path)
        self.assertIn("verdict", r.stdout)
        os.unlink(path)

        # shape-only: score<10 with zero issues is NOT invalid here (semantic rule is the orchestrator's)
        path = write(make_critique("m", issues=[]))
        r = self._run_validator(path)
        self.assertEqual(r.returncode, 0, r.stdout)
        os.unlink(path)

        # skeleton critic -> exit 1
        path = write({"model": "m"})
        r = self._run_validator(path)
        self.assertEqual(r.returncode, 1)
        self.assertIn("critic[0]", r.stdout)
        os.unlink(path)

    def test_wrong_types_exit_1(self):
        bad = make_critique("m")
        bad["overall_score"] = "8"
        env = {"document": "d", "pass": 1, "round": 1, "critics": [bad], "n_valid": 1}
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(env, f)
        r = self._run_validator(path)
        self.assertEqual(r.returncode, 1)
        self.assertIn("overall_score", r.stdout)
        os.unlink(path)
        bad2 = make_critique("m")
        bad2["pass"] = True  # bool is not an int
        env = {"document": "d", "pass": 1, "round": 1, "critics": [bad2], "n_valid": 1}
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(env, f)
        r = self._run_validator(path)
        self.assertEqual(r.returncode, 1)
        self.assertIn("pass", r.stdout)
        os.unlink(path)

    def test_unreadable_exit_1_stderr(self):
        r = subprocess.run(
            [sys.executable, os.path.join(KIT_SCRIPTS, "validate_critique.py"),
             "--file", "/nonexistent/critique.json"],
            capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertTrue(r.stderr.strip())

    def test_orchestrator_enforces_semantic_rule(self):
        # Every critic returns score<10 with zero issues (noise) twice -> all invalid.
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        out_dir = tempfile.mkdtemp(prefix="m2noise-")
        with mock.patch("time.sleep", side_effect=lambda s: None):
            def fake_call(m, key, prompt, timeout_s):
                return json.dumps(make_critique(m["model"], score=9, issues=[], verdict="pass"))
            with mock.patch.object(oc, "call", side_effect=fake_call), \
                 mock.patch("sys.stderr", new=open(os.devnull, "w")):
                rc = oc.run(doc.name, "noise", 1, 1, out_dir, REAL_ENV, 30, 25, REAL_CONFIG)
        os.unlink(doc.name)
        self.assertEqual(rc, 3, "all-noise round must escalate with exit 3")
        data = json.load(open(os.path.join(out_dir, "pass1-round1-noise.json")))
        self.assertEqual(data["n_valid"], 0)


class NT3UnparseableRetry(unittest.TestCase):
    """NT3 — R2 retry (unparseable): <=1 retry, then counted (AC-3)."""

    def test_garbage_then_valid(self):
        p = write_temp_config(single_slot_config())
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        out_dir = tempfile.mkdtemp(prefix="m2retry-")
        calls = []

        def fake_call(m, key, prompt, timeout_s):
            calls.append(1)
            if len(calls) == 1:
                return "not json at all {{{"
            return json.dumps(make_critique("test-model-1", doc="retry", rnd=1, ps=1))

        with mock.patch("time.sleep", side_effect=lambda s: None), \
             mock.patch.object(oc, "call", side_effect=fake_call):
            rc = oc.run(doc.name, "retry", 1, 1, out_dir, {"TEST_KEY": "k"}, 30, 25, p)
        os.unlink(doc.name)
        os.unlink(p)
        self.assertEqual(len(calls), 2, "exactly one retry after the unparseable attempt")
        self.assertEqual(rc, 0)
        data = json.load(open(os.path.join(out_dir, "pass1-round1-retry.json")))
        self.assertEqual(data["n_valid"], 1)

    def test_garbage_twice_excluded(self):
        p = write_temp_config(single_slot_config())
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        out_dir = tempfile.mkdtemp(prefix="m2bad-")
        with mock.patch("time.sleep", side_effect=lambda s: None), \
             mock.patch.object(oc, "call",
                               side_effect=lambda *a: "still not json {{{"), \
             mock.patch("sys.stderr", new=open(os.devnull, "w")):
            rc = oc.run(doc.name, "bad", 1, 1, out_dir, {"TEST_KEY": "k"}, 30, 25, p)
        os.unlink(doc.name)
        os.unlink(p)
        self.assertEqual(rc, 3)
        data = json.load(open(os.path.join(out_dir, "pass1-round1-bad.json")))
        self.assertEqual(data["n_valid"], 0, "unparseable twice -> excluded this round")

    def test_truncation_repaired_counts_without_retry(self):
        # Output-cap truncation is repaired best-effort; a successful repair
        # counts on the first attempt (no retry consumed).
        p = write_temp_config(single_slot_config())
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        out_dir = tempfile.mkdtemp(prefix="m2trunc-")
        calls = []

        def fake_call(m, key, prompt, timeout_s):
            calls.append(1)
            full = json.dumps(make_critique("test-model-1", doc="trunc", rnd=1, ps=1))
            return full[:len(full) - 14]  # cut mid-JSON: unterminated string + missing braces

        with mock.patch("time.sleep", side_effect=lambda s: None), \
             mock.patch.object(oc, "call", side_effect=fake_call):
            rc = oc.run(doc.name, "trunc", 1, 1, out_dir, {"TEST_KEY": "k"}, 30, 25, p)
        os.unlink(doc.name)
        os.unlink(p)
        self.assertEqual(len(calls), 1, "repaired response must count without a retry")
        self.assertEqual(rc, 0)
        data = json.load(open(os.path.join(out_dir, "pass1-round1-trunc.json")))
        self.assertEqual(data["n_valid"], 1)

    def test_bad_candidate_never_counts(self):
        # First candidate parses but fails the full validity check; the valid
        # candidate later in the text must win on the same first attempt.
        p = write_temp_config(single_slot_config())
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        out_dir = tempfile.mkdtemp(prefix="m2cand-")
        calls = []

        def fake_call(m, key, prompt, timeout_s):
            calls.append(1)
            good = json.dumps(make_critique("test-model-1", doc="cand", rnd=1, ps=1))
            return '{"model":"x"} then prose {more braces} then: ' + good

        with mock.patch("time.sleep", side_effect=lambda s: None), \
             mock.patch.object(oc, "call", side_effect=fake_call):
            rc = oc.run(doc.name, "cand", 1, 1, out_dir, {"TEST_KEY": "k"}, 30, 25, p)
        os.unlink(doc.name)
        os.unlink(p)
        self.assertEqual(len(calls), 1, "a bad first candidate must not consume the retry")
        self.assertEqual(rc, 0)
        data = json.load(open(os.path.join(out_dir, "pass1-round1-cand.json")))
        self.assertEqual(data["n_valid"], 1)
        self.assertEqual(data["critics"][0]["model"], "test-model-1",
                         "the later, fully valid candidate must win")


class NT4TransportRetries(unittest.TestCase):
    """NT4 — R3 transport: <=5 tries with growing backoff (AC-3)."""

    def _run(self, behavior, config=single_slot_config(), key="TEST_KEY"):
        p = write_temp_config(config)
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        out_dir = tempfile.mkdtemp(prefix="m2tr-")
        sleeps, calls = [], []
        with mock.patch("time.sleep", side_effect=lambda s: sleeps.append(s)), \
             mock.patch.object(oc, "call", side_effect=behavior), \
             mock.patch("sys.stderr", new=open(os.devnull, "w")):
            rc = oc.run(doc.name, "tr", 1, 1, out_dir, {key: "k"}, 30, 25, p)
        os.unlink(doc.name)
        os.unlink(p)
        return rc, out_dir, sleeps, calls

    def test_429_five_times_absent(self):
        def behavior(m, key, prompt, timeout_s):
            raise urllib.error.HTTPError("http://x", 429, "Too Many Requests", {}, None)
        rc, out_dir, sleeps, _ = self._run(behavior)
        self.assertEqual(rc, 3, "all-fail transport round -> escalation exit 3")
        backoffs = sorted(v for v in sleeps if v > 0)
        self.assertEqual(backoffs, [30, 60, 90, 120], "429 backoff = 30s x attempt")

    def test_429_then_200_counted(self):
        state = {"n": 0}
        def behavior(m, key, prompt, timeout_s):
            state["n"] += 1
            if state["n"] == 1:
                raise urllib.error.HTTPError("http://x", 429, "Too Many Requests", {}, None)
            return json.dumps(make_critique("test-model-1", doc="tr", rnd=1, ps=1))
        rc, out_dir, sleeps, _ = self._run(behavior)
        self.assertEqual(state["n"], 2)
        self.assertEqual(rc, 0)
        data = json.load(open(os.path.join(out_dir, "pass1-round1-tr.json")))
        self.assertEqual(data["n_valid"], 1)

    def test_5xx_backoff(self):
        def behavior(m, key, prompt, timeout_s):
            raise urllib.error.HTTPError("http://x", 500, "Internal Server Error", {}, None)
        rc, out_dir, sleeps, _ = self._run(behavior)
        self.assertEqual(rc, 3)
        backoffs = sorted(v for v in sleeps if v > 0)
        self.assertEqual(backoffs, [8, 16, 24, 32], "5xx/timeout backoff = 8s x attempt")

    def test_deterministic_client_error_no_retry(self):
        n = {"n": 0}
        def behavior(m, key, prompt, timeout_s):
            n["n"] += 1
            raise urllib.error.HTTPError("http://x", 401, "Unauthorized", {}, None)
        rc, out_dir, sleeps, _ = self._run(behavior)
        self.assertEqual(n["n"], 1, "non-429 4xx is not retried")
        self.assertEqual(rc, 3)
        self.assertTrue(all(v == 0 for v in sleeps), "no backoff sleeps for deterministic error")


class NT5NoCrossRoundExclusion(unittest.TestCase):
    """NT5 — a critic invalid in one round participates again next round (AC-3)."""

    def test_invalid_critic_reappears_each_round(self):
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        calls = []
        with mock.patch("time.sleep", side_effect=lambda s: None):
            def fake_call(m, key, prompt, timeout_s):
                calls.append(m["model"])
                if m["model"] == "z-ai/glm-5.2":
                    return "always garbage {{{"
                return json.dumps(make_critique(m["model"], doc="x", rnd=1, ps=1))
            with mock.patch.object(oc, "call", side_effect=fake_call):
                out1 = tempfile.mkdtemp(prefix="m2nr1-")
                rc1 = oc.run(doc.name, "nr", 1, 1, out1, REAL_ENV, 30, 25, REAL_CONFIG)
                out2 = tempfile.mkdtemp(prefix="m2nr2-")
                rc2 = oc.run(doc.name, "nr", 1, 2, out2, REAL_ENV, 30, 25, REAL_CONFIG)
        os.unlink(doc.name)
        self.assertEqual((rc1, rc2), (0, 0))
        glm = [i for i, m in enumerate(calls) if m == "z-ai/glm-5.2"]
        self.assertEqual(len(glm), 4, "2 invalid attempts x 2 rounds — no persistent exclusion")
        for rnd, out in ((1, out1), (2, out2)):
            data = json.load(open(os.path.join(out, f"pass1-round{rnd}-nr.json")))
            self.assertNotIn("z-ai/glm-5.2", [c["model"] for c in data["critics"]])
            self.assertEqual(data["n_valid"], 6)


class NT6RoundCapContract(unittest.TestCase):
    """NT6 — --round-cap validated (0 OK, -1 -> exit 2); no script-side cap enforcement."""

    def _cli(self, args):
        r = subprocess.run([sys.executable, os.path.join(KIT_SCRIPTS, "orchestrate_critique_loop.py")] + args,
                           capture_output=True, text=True)
        return r.returncode

    def test_cli_validation(self):
        self.assertEqual(self._cli(["--doc", "x", "--name", "n", "--pass", "1", "--round", "0"]), 2)
        self.assertEqual(self._cli(["--doc", "x", "--name", "n", "--pass", "1", "--round-cap", "-1"]), 2)
        self.assertEqual(self._cli(["--doc", "x", "--name", "n", "--pass", "1", "--timeout", "0"]), 2)
        self.assertEqual(self._cli(["--doc", "x", "--name", "n", "--pass", "1", "--round-cap", "0", "--round", "1"]), 2)
        self.assertEqual(self._cli(["--doc", "x", "--name", "n", "--pass", "1", "--round", "1"]), 2)

    def test_round_beyond_cap_runs(self):
        # Script-side contract: cap validated, enforced by the sub-skill, never by the script.
        doc = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        doc.write("# t\n")
        doc.close()
        out_dir = tempfile.mkdtemp(prefix="m2cap-")
        with mock.patch("time.sleep", side_effect=lambda s: None), \
             mock.patch.object(oc, "call",
                               side_effect=lambda m, k, p, t: json.dumps(
                                   make_critique(m["model"], doc="cap", rnd=30, ps=1))):
            rc = oc.run(doc.name, "cap", 1, 30, out_dir, REAL_ENV, 30, 25, REAL_CONFIG)
        os.unlink(doc.name)
        self.assertEqual(rc, 0, "--round 30 beyond cap 25 still runs")
        self.assertTrue(os.path.exists(os.path.join(out_dir, "pass1-round30-cap.json")))


class NT7OutputPathAndSchema(unittest.TestCase):
    """NT7 — T9 output path + PLAN.md section-4.3 schema (AC-4)."""

    def test_mocked_round_writes_valid_schema_file(self):
        rc, out_dir, _, _ = run_round(REAL_CONFIG, "nt7")
        self.assertEqual(rc, 0)
        path = os.path.join(out_dir, "pass1-round1-nt7.json")
        self.assertTrue(os.path.exists(path), f"expected {path}")
        data = json.load(open(path))
        self.assertEqual(data["document"], "nt7")
        self.assertEqual(data["pass"], 1)
        self.assertEqual(data["round"], 1)
        self.assertEqual(data["n_valid"], len(data["critics"]))
        self.assertEqual(len(data["critics"]), 7)
        self.assertEqual([c["model"] for c in data["critics"]], REAL_SLOTS)
        self.assertEqual(vc.validate_envelope(data), [], "file must pass the shape authority")

    def test_pass2_round_label(self):
        rc, out_dir, _, _ = run_round(REAL_CONFIG, "nt7b", ps=2, rnd=3)
        self.assertEqual(rc, 0)
        path = os.path.join(out_dir, "pass2-round3-nt7b.json")
        self.assertTrue(os.path.exists(path))


class NT8SubSkill(unittest.TestCase):
    """NT8 — T10 sub-skill covers invoke, triage, stopping (AC-5)."""

    def test_coverage(self):
        text = open(os.path.join(REPO, "kit", "skills", "critique-loop", "SKILL.md")).read()
        low = text.lower()
        for needle in ["orchestrate_critique_loop.py", "--doc", "--pass 1|2",
                       "validate_critique.py", "objective", "needs_clarify",
                       "false positive", "pass 1", "pass 2", "round cap",
                       "escalate", "never excluded across rounds", "clarify"]:
            self.assertIn(needle, low, f"missing '{needle}' in sub-skill")


class NT9SecretScan(unittest.TestCase):
    """NT9 — T11 no secret material in the three new files (AC-6)."""

    def test_no_secret_patterns(self):
        for path in ARTIFACTS:
            text = open(path).read()
            for pat in SECRET_PATTERNS:
                self.assertEqual(pat.findall(text), [], f"{pat.pattern} matched in {path}")

    def test_key_env_names_only(self):
        src = open(os.path.join(KIT_SCRIPTS, "orchestrate_critique_loop.py")).read()
        self.assertIn("key_env", src, "keys must be read via the config's key_env field")


class NT1AC2NonStub(unittest.TestCase):
    """AC-1 — the three artifacts exist and are non-stub."""

    def test_non_stub(self):
        for path in ARTIFACTS:
            self.assertTrue(os.path.exists(path), path)
            text = open(path).read()
            self.assertGreater(len(text), 500, f"{path} looks like a stub")
            self.assertNotIn("NotImplemented", text)
            self.assertNotIn("TODO", text)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
