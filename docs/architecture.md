# v0.1 architecture

Decision date: 2026-10-05. Proposed milestone; inspection and verification are
implemented, the design-editing loop is not yet implemented.

## One complete engineering loop

1. Engineer supplies an existing Git-managed design and bounded change request.
2. Eve captures saved project state, Git context, and engineering unknowns.
3. A model proposes affected objects/files, assumptions, acceptance criteria,
   and requested tool operations through a provider-independent interface.
4. Authorized changes are implemented in an isolated branch/worktree.
5. KiCad checks the candidate; Eve retains reports and revision-bound evidence.
   Failures trigger iteration.
6. Eve presents the diff, unresolved checks, and assumptions. The engineer
   decides whether to merge or release.

Approval belongs to a scope and candidate revision, not a reusable boolean.
Design edits, external model data transfer, and manufacturing release are
distinct decisions. Model statements cannot establish human consent.

## Boundaries

| Component | Responsibility | State |
| --- | --- | --- |
| CLI | JSON results and exit codes | Implemented |
| Project context | On-disk inventory, SHA-256, Git HEAD/status | Implemented |
| KiCad CLI adapter | Native/Flatpak discovery, bounded subprocesses | Implemented |
| Verification | Recorded ERC/DRC runs | Implemented |
| Workspace manager | Isolated candidate, review diff | Planned |
| PCB adapter | Official IPC, explicit instance selection | Planned |
| Proposal/provider | Typed proposals and tool calls | Planned |
| MCP adapter | Optional stdio transport using official SDK | Planned |

Python 3.11+, standard library core, local JSON artifacts. Subprocess arguments
are lists, never shell strings. Explicit backend selection prevents a silent
switch when diagnosing differing native/Flatpak versions. Current checks operate
on saved files, expose no design mutations, and do not call a model or commit.

## Next increments

Add candidate worktree management with dirty-checkout preservation and a review
bundle tied to hashes. Expose inspect/check through the official MCP SDK after
reviewing a pinned dependency tree. Connect one external model client to those
tools; avoid building a general-purpose agent framework.

Then prove one PCB edit: inspect and move a footprint through official IPC in an
explicitly selected KiCad 10 instance. Use undo transactions, save only the
isolated candidate, run DRC, and show the diff. Test stale state, wrong instances,
cancelled operations, and failed saves.

Schematic editing requires a separate decision: KiCad 9/10 IPC has no schematic
editor API. Evaluate audited reuse or a lossless parser with round-trip fixtures
and ERC, not ad hoc text replacements. Do not depend on development-only KiCad
11 capabilities. Compare a Konnect integration with new implementation before
duplicating its editing work.

Rules checks cannot validate a complete physical design. Human review includes
power, ratings, datasheets, grounding, layout, thermal behavior, assembly, and
test requirements. Simulation is a separate adapter with its own model evidence.
Manufacturing exports and remote services are outside v0.1.
