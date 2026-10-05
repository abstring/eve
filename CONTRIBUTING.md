# Contributing

Keep changes small and reviewable. Explain the engineering problem, behavior,
and validation. Preserve existing work; use a separate branch/worktree for
candidate design edits. Do not automatically stage, commit, reset, or publish
an engineer's design.

Run `PYTHONPATH=src python3 -m unittest discover -s tests -v`. For KiCad adapter
changes, run the opt-in live tests in the README. Test meaningful engineering
invariants and failure paths: edits, stale state, tool output, and traceability.

Keep providers and transports outside the core. Before adding a dependency or
copying code, record its exact version/revision, license, dependency tree, and
notices in `docs/licensing.md`. Contributions are AGPL-3.0-only. Do not copy
noncommercial or ambiguously licensed code into Eve.
