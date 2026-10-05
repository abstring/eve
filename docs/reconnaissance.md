# KiCad integration reconnaissance

Inspected 2026-10-05. These are observations and design decisions, not a claim
that Eve implements all capabilities of the referenced projects.

## Local environment

- Initial checkout: clean `main`, upstream `origin/main`, initial revision
  `8f9627a007a62ce542acc7beafea634d6e0cea1c`; only README and GPLv3 LICENSE.
- Python 3.14.7 and Git on the host. No host `kicad-cli`, `pcbnew`, `kipy`, or MCP
  Python package was discoverable during initial inspection.
- KiCad **10.0.6** installed system-wide as Flatpak `org.kicad.KiCad` from Flathub.
  `flatpak run --command=kicad-cli org.kicad.KiCad version` works.
- Installed ERC and DRC help confirm JSON reports, severity selection, and
  `--exit-code-violations`. Native package query found no KiCad RPM.
- Flatpak permissions include home, `/media`, `/run/media`, X11 and IPC.
  Its `TMPDIR` is `/var/tmp`. Do not assume host temporary paths or IPC sockets
  are visible in the sandbox.
- `pcbnew` is available inside the Flatpak. It was used only to generate our
  original test boards, not added as an Eve dependency.
- `kipy` was also absent from the Flatpak's Python interpreter. IPC bindings
  remain a future optional dependency.

## Official interfaces

| Interface | Fit | Limits / decision |
| --- | --- | --- |
| `kicad-cli` | Saved-file ERC/DRC and future exports | Use now; bounded subprocess calls and original JSON evidence |
| IPC / `kicad-python` (`kipy`) | Stable external PCB editing API | Preferred future mutation adapter; explicit GUI instance selection |
| Legacy SWIG `pcbnew` | Existing board automation | Useful for evaluating fixtures, not the foundation for new plugins |
| Direct schematic file editing | Possible offline schematic changes | Defer until a lossless, audited editing path has round-trip and ERC coverage |

The [versioned KiCad 10 CLI manual](https://docs.kicad.org/10.0/en/cli/cli.html)
describes the exact command surface installed here. DRC must not be invoked with
`--save-board` in an inspection/check path. We also omit `--refill-zones`; checking
saved geometry and comparing schematic parity are distinct capabilities.

The [official add-on guide](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/)
states that KiCad 9/10 IPC operates against a running GUI and supports PCB editor
plugins. Headless IPC, plotting/exporting IPC, and schematic-editor plugins are
documented for KiCad 11. The [bindings documentation](https://docs.kicad.org/kicad-python/)
defaults to a development version: documentation mentioning `headless=True` is
not evidence that KiCad 10 supports it. Feature/version probing is required.

The [official API index](https://dev-docs.kicad.org/en/apis-and-binding/)
directs new plugin development toward IPC rather than legacy PCB scripting.
No running GUI IPC connection was attempted in this scaffold. Flatpak socket
visibility and instance selection need a dedicated integration test later.

## Existing MCP approaches

| Project | Approach inspected | License finding / Eve decision |
| --- | --- | --- |
| [lamaalrajih/kicad-mcp](https://github.com/lamaalrajih/kicad-mcp) | Python MCP tools; board/file workflows; metadata includes MCP, FastMCP, pandas, YAML and XML packages | MIT; reference only, do not import its dependency tree for a three-command core |
| [fsbondtec/kicad-mcp](https://github.com/fsbondtec/kicad-mcp) | Related Python implementation with Linux support | MIT; reference only |
| [mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server) | TypeScript/Python, legacy SWIG board backend, broad schematic/PCB tooling | Current upstream MIT; reference only |
| [mixelpixx/Konnect](https://github.com/mixelpixx/Konnect) | Rust successor; official PCB IPC, direct schematic S-expression editing, CLI verification, MCP transport | AGPLv3 license text; evaluate reuse before building an extensive mutation layer |
| [miyosuda/kicad-mcp-server](https://github.com/miyosuda/kicad-mcp-server) | Fork of the TypeScript/Python server | Noncommercial/educational restriction in LICENSE; exclude code |

License findings come from actual LICENSE files, not repository descriptions.
The current mixelpixx upstream MIT license must not be confused with the
restricted fork. Their implementations were inspected as references; none was
installed, executed, or copied into Eve. README capability claims are not
independent validation. See [licensing.md](licensing.md) for audited revisions.

## Decision

Build a small, original Python core with a CLI adapter first. Native and Flatpak
KiCad discovery makes it useful on this workstation immediately. Keep model
providers and an optional official MCP SDK transport outside that core. Add
Git-isolated edits and official IPC next, with a separate schematic editing
decision. Avoid large tool catalogs, two language runtimes, web infrastructure,
and dependency adoption until they solve a demonstrated requirement.

## Initial validation

On the environment above, all 17 tests passed: 14 unit tests and three opt-in
live checks (outlined PCB pass, absent-outline PCB violations, blank-schematic
ERC pass). Input hashes remained unchanged in all live checks. Failure-path
tests cover timeouts, malformed/missing reports, changed inputs, symlinked
artifacts, paths outside the project, and backend fallback.

An isolated virtual environment installed the editable package successfully;
a wheel built successfully and contained the full license with
`License-Expression: AGPL-3.0-only` and no `Requires-Dist` runtime entries.
The installed `eve doctor` detected the Flatpak. Linux CI is configured for
Python 3.11/3.14; remote CI results were not available during initial validation.
