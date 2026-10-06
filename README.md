# Eve

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/branding/logo/eve-logo-dark-768.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/branding/logo/eve-logo-light-768.png">
    <img src="assets/branding/logo/eve-logo-light-768.png" alt="eve.engineer — Eve inspecting a PCB, framed by natural leaves" width="640">
  </picture>
</p>

**She took the knowledge; then she shared it with everyone.**

Open-source, Linux-native AI engineering for KiCad ECAD and FreeCAD MCAD.

Eve is being built to help engineers design, analyze, modify, verify, and iterate
on real electronic and mechanical hardware, bringing KiCad electrical design
and FreeCAD mechanical design into a shared workflow. She is model-agnostic,
Git-native, and designed
around an engineer-in-the-loop philosophy:

**AI proposes and implements. Tools verify. Humans own the engineering decisions.
Physics gets the final vote.**

**Your designs are yours. Eve's AGPL license covers Eve's software—not your
hardware designs or generated outputs. Keep your work private, sell it, or
share it under your own terms. No required publication, attribution to Eve,
or continued use of Eve.** See [output licensing](docs/licensing.md#designs-and-generated-outputs)
for the full policy and third-party material considerations.

**Attribution is appreciated where practicable, never required.** If Eve helps
with your design, consider a note such as "Co-designed with eve.engineer" in
your documentation or on the hardware. Optional [15 × 15 mm hardware artwork](assets/branding/hardware/README.md)
is available for KiCad silkscreen and FreeCAD raised or recessed marking.

## Project status

This is the `0.1.0.dev0` foundation, not a finished autonomous design agent.
It provides working local tools for environment discovery, project inspection,
and recorded KiCad electrical/design rule checks. Model connections, MCP,
schematic editing, PCB mutation, and FreeCAD integration are planned. The current
CLI implements KiCad workflows; MCAD, manufacturing, and firmware interface
features below describe the intended scope, not capabilities already available.

The first milestone is one reviewable loop: inspect a small existing design,
propose a bounded change, implement it in an isolated Git branch/worktree,
run KiCad checks, and present the diff and evidence for an engineer to accept.

## Where Eve is going

- **AI-assisted ECAD and MCAD:** design, edit, and verify electronics in KiCad
  and mechanical parts and assemblies in FreeCAD.
- **Bidirectional co-design:** exchange and reconcile electrical and mechanical
  designs, including PCB outlines, mounting holes, component envelopes,
  enclosures, and clearance constraints. Changes in either discipline should
  remain reviewable in the other.
- **Procedural 3D parts:** create parameterized parts from manufacturer
  datasheets, with source references, dimensions, tolerances, and explicit
  assumptions available for review.
- **Auditing and learning:** inspect and verify electrical and mechanical
  designs, explain findings, and tutor learners through the engineering
  decisions behind a design.
- **Firmware interface handoff:** create interface control documents (ICDs)
  and matching firmware stubs and starter templates for mainstream
  microcontrollers such as RP2040, ESP32, and STM32. Tie GPIO assignments and
  peripheral interfaces to the hardware design so engineers can bring up a
  board with a small "hello world" that exercises its intended connections.
- **Model choice:** connect to models through an OpenAI-compatible API format,
  keeping engineering tools independent of any particular model or provider.
- **Sourcing and manufacturing preparation:** help select and source parts,
  prepare PCB stackups and fabrication packages, and create mechanical drawings
  and CAM packages for machine shops and automated cutting services such as
  SendCutSend. Packages should include the relevant materials, tolerances, and
  verification evidence for the chosen process and supplier.

More to come as real projects shape the workflow. Across both disciplines,
engineers review changes and approve design and manufacturing decisions.

### Firmware interface scope

Eve is a hardware design platform. Its planned firmware assistance supports
accurate interface control and a handoff to the engineer's chosen coding
environment. An ICD should identify signals, MCU pins and GPIO assignments,
directions, voltage levels, peripheral mappings, timing constraints, and safe
startup states, with references to the hardware revision and relevant datasheets.
Matching templates should keep those assignments traceable to the ICD and make
unresolved assumptions explicit.

For example, an RP2040 board could receive a minimal bring-up project that
toggles the designated LED, reads an intended input, and initializes the
specified serial or sensor interface on the assigned GPIOs. These small
examples and stubs are starting points for checking the documented interfaces;
they require engineer review and testing on the actual hardware.

Comprehensive firmware design, application logic, production drivers, and a
replacement for the engineer's software toolchain are outside Eve's scope.
Engineers take the exported ICDs and templates into their own development
environment for further firmware engineering.

## Try it on Linux

Requirements: Python 3.11+, Git for revision context, and KiCad 9+ for checks.
Initial live validation used KiCad 10.0.6 through Flatpak. Native `kicad-cli`
is preferred; Eve falls back to the `org.kicad.KiCad` Flatpak.
FreeCAD is the planned MCAD integration target and is not required by the
current CLI.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/eve doctor
.venv/bin/eve inspect /path/to/hardware-project
.venv/bin/eve check /path/to/hardware-project/main.kicad_sch \
  --project-root /path/to/hardware-project
.venv/bin/eve check /path/to/hardware-project/main.kicad_pcb \
  --project-root /path/to/hardware-project
```

The core has no third-party runtime Python dependencies. Run directly from
this checkout without installing packages:

```sh
PYTHONPATH=src python3 -m eve doctor
PYTHONPATH=src python3 -m eve inspect .
PYTHONPATH=src python3 -m eve check tests/fixtures/outlined.kicad_pcb
```

Commands return JSON. `doctor` reports executable discovery and host IPC binding
availability; it does not establish an IPC connection. Use `--backend native`
or `--backend flatpak` with `doctor`/`check` to choose explicitly. Flatpak must
already have access to the project and output directory; Eve does not change
sandbox permissions. Checks have a 120-second timeout, adjustable with `--timeout`.

## Inspectable verification

`check` chooses ERC for `.kicad_sch` and DRC for `.kicad_pcb`. Each run creates
`<project-root>/.eve/runs/<id>/` containing:

- `report.json`: KiCad's original report, when the tool produces one.
- `manifest.json`: command, version, timestamps, process result, stdout/stderr,
  report hash, Git HEAD/status, and design input hashes before and after.

The project root defaults to the input file's directory. Pass it explicitly for
hierarchical schematics or designs spread across subdirectories. Add `.eve/` to
your hardware repository's `.gitignore`; retain selected evidence with a review.
Run directories are never reused or overwritten.

Exit codes: **0** check passed, **1** rule violations, **2** operational error or
changed inputs. Inspection works without Git and records unavailable context.
Dirty and unborn checkouts are recorded without cleanup, commits, or resets.

Checks request all severities and do not request board saving or zone refill.
Hashing captures KiCad design/library files and library tables under the project
root, excluding Git, artifacts, virtual environments, and dependency directories.
Symlinked design files are rejected. External libraries, environment variables,
GUI state, and non-KiCad assets are not captured; manifests are traceability
records rather than complete reproducible-build snapshots. Concurrent changes
to captured inputs invalidate the result.

A passing rules check is evidence about the saved design and configured rules.
It does not guarantee electrical correctness, manufacturability, thermal
performance, or safety. Review exclusions and rule settings in the raw report.
Schematic/PCB parity checking and copper-zone refill are not enabled yet.

## Small by design

```text
src/eve/
  cli.py           JSON command interface
  project.py       design inventory, hashes, Git context
  kicad.py         native/Flatpak subprocess adapter
  verification.py recorded ERC/DRC runs
docs/
  architecture.md v0.1 boundaries and next milestones
  reconnaissance.md integration research and local findings
  licensing.md    license decision and dependency review
tests/
  test_eve.py      behavior and failure-path tests
  test_live.py     optional installed-KiCad integration tests
  fixtures/       minimal original KiCad test designs
```

Models will use the same engineering tools as the CLI. Optional MCP transport
and OpenAI-compatible API adapters can be added without embedding a particular
model SDK in the core. A planned FreeCAD adapter will expose mechanical design
and verification tools alongside the KiCad adapter, with explicit exchange
artifacts and units at the ECAD/MCAD boundary. Prefer the official KiCad IPC API
for future PCB edits; retain the CLI for
headless checks. No web service, database, containers, or agent framework is
needed for the first milestone. See [architecture](docs/architecture.md) and
[integration research](docs/reconnaissance.md).

## Development

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
EVE_LIVE_TESTS=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Live tests copy fixtures to a temporary directory under your home directory for
Flatpak access. They test passing DRC, failing DRC, passing ERC, and unchanged
design inputs. Fixtures exercise integration plumbing, not production circuits.
CI tests Linux package installation on Python 3.11 and 3.14.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Software development attribution

Eve's code is co-developed by human developers with assistance from
**OpenAI GPT-6.1 Sol**. AI is used to help develop this software, including
implementation, research, documentation, and validation. Human developers
remain responsible for reviewing changes and making engineering decisions.

AI can introduce mistakes, incorrect assumptions, or misconceptions that human
developers also miss. Human review and passing tests do not guarantee that the
software is correct or that its engineering conclusions are sound. Independently
verify results before relying on them in a hardware design.

We record development model changes below, retaining earlier entries so this
disclosure reflects the project's history. This attribution concerns development
of Eve itself; it does not restrict which models engineers can use with Eve.

| Recorded date | Model | Development use |
| --- | --- | --- |
| 2026-10-05 | OpenAI GPT-6.1 Sol | Initial software development assistance |

## License

Eve's software is **AGPL-3.0-only**; see [LICENSE](LICENSE). Commercial use is
permitted under its terms.

**Eve's license does not apply to hardware designs or other outputs created,
edited, or verified with Eve. Your designs are yours.** Schematics, PCBs, mechanical models, drawings,
fabrication and CAM packages, ICDs, reports, and generated firmware stubs and
templates can remain private, proprietary, commercial, or open source under
terms you choose. **Using Eve imposes no requirement to publish those outputs,
license them under AGPL, attribute Eve, or keep using Eve.**

If generated output incorporates Eve-owned code or templates, the project
grants permission to use, modify, and redistribute that material as part of
the output under terms you choose, without AGPL obligations. This permission
does not cover Eve's software itself or third-party material, whose own
licenses remain applicable. See the [output licensing policy](docs/licensing.md#designs-and-generated-outputs).

The [dependency/license review](docs/licensing.md) records the decision.
No code from the investigated MCP implementations has been incorporated.

Project logo and icon downloads: [brand assets](assets/branding/README.md).[^artwork]

[^artwork]: Logo inspired by Peter Paul Rubens's *Adam and Eve* (1598–1600), City of Antwerp Collection, [Rubenshuis, Antwerp, Belgium](https://www.rubenshuis.be/en/peter-paul-rubens-adam-and-eve). The museum image is public domain. [Artwork credits and image sources](assets/branding/source/artwork-credits.md).
