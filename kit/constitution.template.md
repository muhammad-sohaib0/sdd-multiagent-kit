# Constitution — Governing Principles

This is the project's constitution: a short set of principles that stay fixed for the life of the project and that every milestone's documents must be consistent with. Where the spec answers "what does this milestone need," the constitution answers "what does this project never compromise on, regardless of milestone."

This starter set is meant to be adopted as-is or edited once at project start, not rewritten per milestone. Once adopted, it is written to `outputs/constitution.md` and reused for every milestone; it changes only through the Amendment Process (Article VII).

**Article I — Standalone-First:** Every capability starts as an independently testable unit before it's wired into the larger system. Nothing is built directly inside application glue code that couldn't be pulled out and tested on its own.

**Article II — Observable Interfaces:** Every unit exposes its behavior through an interface that can be inspected and scripted from the outside — command-line, API, or equivalent. Behavior that can only be observed by reading source code is a defect, not a design choice.

**Article III — Tests Before Implementation:** No implementation code is written before its tests exist, have been reviewed, and are confirmed to fail first. This is enforced through the task ordering in §7.2's `tasks.md`, not left to discipline alone.

**Article IV — Simplicity by Default:** Start with the smallest structure that could work. Anything more requires the documented justification described in §5.4, not a default assumption that more structure is safer.

**Article V — Framework Trust:** Use the tools and frameworks already in play directly. A wrapper around them needs a specific, stated reason to exist.

**Article VI — Real-World Testing:** Prefer real dependencies over mocks wherever practical. Contract tests are written before the implementation they're testing.

**Article VII — Amendment Process:** Changing this constitution requires a written reason for the change and a note on what it might affect downstream. Amendments are logged as ADRs (§8.2), never made silently.

---

These are immutable within a project once adopted — no milestone's critique loop is allowed to argue its way around them; they are a frozen node. They can only change through the amendment process in Article VII, which is itself deliberately slower and more visible than any single milestone's revision cycle.

**Override convention line (optional):** to change the Simplicity default (number of standalone components per milestone, default 3), append `simplicity_default: N` below, then record an ADR.