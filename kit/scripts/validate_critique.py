#!/usr/bin/env python3
"""Validate a critique-log JSON against the SDD critique response schema.

Schema authority: the kit's PLAN.md section 4.3 (critique response schema).

Required per critic: model (str), document (str), round (int), pass (int),
overall_score (int), scores (all five keys, ints: clarity, completeness,
edge_case_coverage, internal_consistency, testability), issues (array — an
omitted issues field is invalid; an empty array is the only valid "no issues"
form; each issue requires section, category, problem), verdict (str).
Optional per issue: why_it_matters, suggested_fix.
Top-level envelope: document (str), pass (int), round (int),
critics (list), n_valid (int == len(critics)).

Shape only — no enum constraints (field values are not restricted to fixed
sets). Semantic validity (unparseable, or overall_score < 10 with zero issues)
is the orchestrator's rule, not this script's.

Exit 0 if the file is valid, 1 if any malformed entries are found or the input
cannot be read/parsed.
"""
import argparse
import json
import sys

REQUIRED_CRITIC = [
    "model", "document", "round", "pass", "overall_score",
    "scores", "issues", "verdict",
]
SCORE_KEYS = [
    "clarity", "completeness", "edge_case_coverage",
    "internal_consistency", "testability",
]
OPTIONAL_ISSUE = ["why_it_matters", "suggested_fix"]
REQUIRED_ISSUE = ["section", "category", "problem"]


def _is_int(v):
    """True for ints; bools are not ints for schema purposes."""
    return isinstance(v, int) and not isinstance(v, bool)


def validate_single(o, idx):
    """Return a list of problem strings for one critic dict."""
    problems = []
    if not isinstance(o, dict):
        return [f"critic[{idx}]: not an object"]
    for k in REQUIRED_CRITIC:
        if k not in o:
            problems.append(f"critic[{idx}]: missing required field '{k}'")
    if "model" in o and not isinstance(o["model"], str):
        problems.append(f"critic[{idx}]: model not a string")
    if "document" in o and not isinstance(o["document"], str):
        problems.append(f"critic[{idx}]: document not a string")
    if "round" in o and not _is_int(o["round"]):
        problems.append(f"critic[{idx}]: round not an int")
    if "pass" in o and not _is_int(o["pass"]):
        problems.append(f"critic[{idx}]: pass not an int")
    if "verdict" in o and not isinstance(o["verdict"], str):
        problems.append(f"critic[{idx}]: verdict not a string")
    if "overall_score" in o and not _is_int(o["overall_score"]):
        problems.append(f"critic[{idx}]: overall_score not int")
    s = o.get("scores")
    if isinstance(s, dict):
        for k in SCORE_KEYS:
            if k not in s:
                problems.append(f"critic[{idx}]: scores missing '{k}'")
            elif not _is_int(s[k]):
                problems.append(f"critic[{idx}]: scores.{k} not int")
    elif "scores" in o:
        problems.append(f"critic[{idx}]: scores not an object")
    issues = o.get("issues")
    if not isinstance(issues, list):
        if "issues" in o:
            problems.append(f"critic[{idx}]: issues not a list")
    else:
        for j, it in enumerate(issues):
            if not isinstance(it, dict):
                problems.append(f"critic[{idx}].issues[{j}]: not an object")
                continue
            for k in REQUIRED_ISSUE:
                if k not in it:
                    problems.append(f"critic[{idx}].issues[{j}]: missing '{k}'")
    return problems


def validate_envelope(data):
    """Return a list of problem strings for the top-level wrapper."""
    problems = []
    if not isinstance(data, dict):
        return ["top level must be an object"]
    if "document" not in data or not isinstance(data["document"], str):
        problems.append("top-level 'document' must be a string")
    if "pass" not in data or not _is_int(data["pass"]):
        problems.append("top-level 'pass' must be an int")
    if "round" not in data or not _is_int(data["round"]):
        problems.append("top-level 'round' must be an int")
    critics = data.get("critics")
    if not isinstance(critics, list):
        problems.append("top-level 'critics' must be a list")
    else:
        nv = data.get("n_valid")
        if not _is_int(nv):
            problems.append("top-level 'n_valid' must be an int")
        elif nv != len(critics):
            problems.append(f"top-level 'n_valid' {nv} != len(critics) {len(critics)}")
        for i, c in enumerate(critics):
            problems.extend(validate_single(c, i))
    return problems


def validate_data(data):
    problems = validate_envelope(data)
    for p in problems:
        print("invalid:", p)
    return 1 if problems else 0


def validate_file(path):
    try:
        data = json.load(open(path))
    except (OSError, ValueError) as e:
        print(f"cannot read '{path}': {e}", file=sys.stderr)
        return 1
    return validate_data(data)


def main():
    ap = argparse.ArgumentParser(description="Validate a critique-log JSON against the SDD schema")
    ap.add_argument("--file", help="path to critique-log JSON (or '-' for stdin)")
    a = ap.parse_args()
    if a.file in (None, "-"):
        path = sys.stdin
    else:
        path = a.file
    if isinstance(path, str):
        return validate_file(path)
    try:
        data = json.load(path)
    except ValueError as e:
        print(f"cannot parse stdin: {e}", file=sys.stderr)
        return 1
    return validate_data(data)


if __name__ == "__main__":
    sys.exit(main())