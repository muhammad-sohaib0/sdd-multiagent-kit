# Examples

This directory shows the SDD Multi-Agent Kit in action: a small, self-contained sample project you can either study to learn the kit's workflow or run the kit against to produce your own spec-to-build pipeline.

## `sample-project/`

A small, dependency-free Python 3 command-line tool called `quote` that prints programming quotes to the terminal and manages a plain-text store. It is a teaching example: realistic enough to exercise the kit's loop (input handling, a small data store, output formatting, exit codes), small enough to demo in minutes, and runnable anywhere with a standard Python 3 interpreter.

Inside the folder you get two things:

- `PLAN.md` — the sample brief, written in the kit's designated brief format with the required headings (`Brief`, `Requirements`, `Non-negotiable`, `Out of scope`, `Success criteria`). It is self-contained: nothing outside the folder is needed to read or use it.
- `outputs/milestones/milestone_1/` — one completed five-document set (spec, plan, tasks, workflow, tests) demonstrating the output shape the kit produces for every milestone. Use it as a template for your own projects.

### Run the kit against the sample brief

From the repo root, with the kit installed in your tool (see [docs/GUIDE.md](../docs/GUIDE.md) §2), invoke the skill directly:

```
/sdd   # then point it at examples/sample-project/PLAN.md
```

Alternatively, drive the critique engine against a produced document. First make sure the provider keys (`NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, `OLLAMA_API_KEY`) are present in the environment as documented in [docs/GUIDE.md](../docs/GUIDE.md) §2, then run:

```bash
python3 kit/scripts/orchestrate_critique_loop.py \
  --doc examples/sample-project/outputs/milestones/milestone_1/spec_milestone_1.md \
  --name example_spec --pass 2 --round 1
```

### How the example set was produced

The shipped five-document set is a **hand-crafted representative**: it was written by hand to mirror the kit's output shape exactly, so it is stable, readable, and safe to commit. It is not the output of a live kit run, and it is not meant to be regenerated in place — the kit has no overwrite protection, so running `/sdd` against `PLAN.md` in this folder would replace the example files. To generate your own live set, copy `sample-project/` to a fresh directory first and run the kit there.

### Notes

- The example ships the *output shape*, not a full implementation; no `quote.py` or other source is included.
- The `tasks` document's build steps are illustrative and reference files that need not exist in this repo.
- Nothing here needs API keys, secrets, or the network — it is a local, dependency-free CLI using only Python's standard library.

For the full usage walkthrough, see [docs/GUIDE.md](../docs/GUIDE.md).