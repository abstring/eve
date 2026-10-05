# Integration fixtures

Original minimal designs created for Eve on 2026-10-05, licensed AGPL-3.0-only.
`empty.kicad_pcb` has no outline and should fail DRC. `outlined.kicad_pcb` has a
closed 20 mm square outline and should pass DRC. KiCad 10.0.6's bundled pcbnew
generated these boards and their project settings. They contain no components.
`blank.kicad_sch` is an empty schematic to exercise ERC reporting.

These are adapter smoke tests, not electrical design examples. Keep paired
project files: they establish stable rule settings during live checks.
