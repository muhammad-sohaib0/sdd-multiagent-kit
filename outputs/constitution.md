# The SDD Multi-Agent Kit — Constitution

Adopted for the kit's own build (bootstrap run) per `PLAN.md` §6 and `BOOTSTRAP.md` §3.4. These principles are fixed for the life of this project. No milestone's critique loop may argue its way around them; they change only through Article VII.

---

## Article I — Standalone-First

Every capability starts as an independently testable unit before it is wired into the larger system. Nothing is built directly inside application glue code that could not be pulled out and tested on its own.

## Article II — Observable Interfaces

Every unit exposes its behavior through an interface that can be inspected and scripted from the outside — command-line, API, or equivalent. Behavior that can only be observed by reading source code is a defect, not a design choice.

## Article III — Tests Before Implementation

No implementation code is written before its tests exist, have been reviewed, and are confirmed to fail first. Enforced through the task ordering in each milestone's `tasks.md`, not left to discipline alone.

## Article IV — Simplicity by Default

Start with the smallest structure that could work. Anything more requires a documented justification in the milestone's `plan.md`, not a default assumption that more structure is safer.

## Article V — Framework Trust

Use the tools and frameworks already in play directly. A wrapper around them needs a specific, stated reason to exist.

## Article VI — Real-World Testing

Prefer real dependencies over mocks wherever practical. Contract tests are written before the implementation they test.

## Article VII — Amendment Process

Changing this constitution requires a written reason for the change and a note on what it might affect downstream. Amendments are logged as ADRs (`history/adr/`), never made silently.