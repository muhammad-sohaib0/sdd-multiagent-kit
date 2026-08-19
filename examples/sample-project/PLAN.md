# PLAN — Quote CLI

## Brief

Build a small, dependency-free command-line tool called `quote` that prints a programming-related quote to the terminal. It is a teaching example for the SDD Multi-Agent Kit, so keep it tiny but real: it should exercise enough surface (input handling, a small data store, output formatting, exit codes) to demonstrate the kit's milestone workflow, yet remain completable in a demo and runnable anywhere with a standard Python 3 interpreter.

## Requirements

1. Running `quote` (no arguments) prints a random programming quote and exits `0`.
2. Running `quote --list` prints all available quotes, one per line, and exits `0`.
3. Running `quote --add "some quote"` appends a new quote to the local store and prints a confirmation.
4. The store lives in a plain text file, one quote per line, at a well-known location (a user-data directory). It must be created on first use.
5. Unknown flags or missing arguments print a short usage message to stderr and exit `2`.
6. Quotes are plain strings; the tool must not require any third-party packages (stdlib only).

## Non-negotiable

- Python 3, standard library only (no dependencies).
- Observable CLI contract (flags + exit codes) as specified above.
- A minimal test suite (written before implementation) covering the flag parsing, the store file lifecycle, and the exit codes.
- Local, no network, no secrets.

## Out of scope

- Concurrency/locking on the store file.
- Remote quote sources or services.
- A fancy TUI; plain terminal text is enough.

## Success criteria

- A user can run the kit against this `PLAN.md` and produce a spec, plan, tasks, workflow, and tests, then a small `quote` implementation that passes those tests and matches the CLI contract above.