# License decision and dependency review

Reviewed 2026-10-05. Eve's new implementation and documentation are licensed
**AGPL-3.0-only**. The full, unmodified text in `LICENSE` was fetched from
[GNU's canonical AGPLv3 text](https://www.gnu.org/licenses/agpl-3.0.txt).
Package metadata uses the same SPDX identifier.

The initial checkout carried GPLv3. This revision adopts the requested network
copyleft direction for the project; earlier GPL grants are not withdrawn.
The scaffold is original code, with no copied MCP or KiCad library source.
Our minimal test designs contain no third-party symbols, footprints, or models.

## Adopted software

| Item | Relationship | License / assessment |
| --- | --- | --- |
| Python standard library | Core runtime | PSF license family; compatible for this use |
| setuptools >=77 | Isolated build tool, not runtime dependency | MIT; compatible |
| Git | Separately installed executable, read-only queries | GPLv2; not linked, vendored, or distributed by Eve |
| KiCad 10.0.6 | Separately installed executable, CLI calls | KiCad GPLv3-or-later; not linked or bundled |
| Flatpak | Separately installed optional launcher | Not linked or distributed by Eve |

The Python package declares **no third-party runtime dependencies**. Subprocess
invocation of installed tools does not copy those tools into Eve's package.
This decision covers this scaffold, not a future bundled installer. Bundling
executables, adding library bindings, or copying code requires a fresh review.

Primary sources: [Python licensing](https://docs.python.org/3/license.html),
[setuptools LICENSE](https://github.com/pypa/setuptools/blob/main/LICENSE),
[KiCad licenses](https://www.kicad.org/about/licenses/), and AGPLv3 sections 5/13
in our LICENSE. MIT reuse requires preservation of notices; GPLv3 and AGPLv3
have explicit combination provisions in section 13. No such combined code is
present in this scaffold.

## Reference-only review

License files were read on the review date. GitHub revisions below were recorded
from repository metadata to make later rechecks possible. Before any reuse,
review the exact files being copied, copyright notices, submodules, assets, and
the pinned transitive dependency tree; repository-level labels are insufficient.

| Reference | Observed license | Revision / evidence | Adoption |
| --- | --- | --- | --- |
| lamaalrajih/kicad-mcp | MIT | [`98c9ea41`](https://github.com/lamaalrajih/kicad-mcp/blob/98c9ea41cb393393a8bafd157a93e84431e00afb/LICENSE) | None |
| fsbondtec/kicad-mcp | MIT | [`c05b15f5`](https://github.com/fsbondtec/kicad-mcp/blob/c05b15f565f1d3876390d8620dcd3157ed7aa02d/LICENSE) | None |
| mixelpixx/KiCAD-MCP-Server | MIT | [`cbb59a62`](https://github.com/mixelpixx/KiCAD-MCP-Server/blob/cbb59a6203997f5e916be7e0480d63fe5519134a/LICENSE) | None |
| miyosuda/kicad-mcp-server | Noncommercial/educational restriction | [`695bc265`](https://github.com/miyosuda/kicad-mcp-server/blob/695bc265d737cf3857da01eb5fd1a459fd9ee34c/LICENSE) | Excluded |
| mixelpixx/Konnect | AGPLv3 text | [`9488e5f0`](https://github.com/mixelpixx/Konnect/blob/9488e5f09717cb508cb25779dc16586d1f06f758/LICENSE) | None |
| Official kicad-python bindings | MIT | [LICENSE](https://gitlab.com/kicad/code/kicad-python/-/blob/main/LICENSE) | Planned only |

The restricted fork is not suitable for unrestricted open-source redistribution.
The MIT references and official bindings present no license-family conflict with
AGPLv3, provided their notices are retained on actual reuse. Konnect is a possible
AGPL integration candidate; its commercial-license offering does not replace
the obligations or permissions of the actual open-source license.

Neither `kipy` nor the MCP SDK is installed as an Eve dependency. Their released
versions and complete dependency trees remain unaudited for adoption. The same
applies to optional schematic libraries and model SDKs. Add versioned findings
here before adding an extra, vendored source, or runtime package.

## Designs and generated outputs

**Your designs are yours. Eve's AGPL license applies to Eve's software, not to
hardware designs or other outputs created, edited, inspected, or verified using
it.** This includes
schematics, PCB layouts, mechanical parts and assemblies, drawings, fabrication
and CAM packages, interface control documents, reports, and generated firmware
stubs and templates.

**Those outputs may be kept private or distributed under proprietary, commercial,
or open-source terms chosen by their rights holders.** Using Eve requires no
publication of designs or outputs, AGPL licensing of them, attribution to Eve,
or continued use of Eve. Exported projects are independent of Eve.

### Additional permission for Eve-owned output material

As an additional permission under AGPLv3 section 7, the copyright holders of
Eve-owned code and templates included in generated output permit that material
to be used, modified, and redistributed as part of the output under terms of
the recipient's choice, without AGPL obligations. This permission applies only
to material for which Eve's contributors hold the necessary rights. It does
not relicense Eve's application, copies or modifications of the application,
or third-party material.

Component libraries, models, SDK examples, and other third-party material retain
their own licenses. Eve's output policy does not override those licenses or
grant rights that their owners have not granted. Future output templates must
identify their provenance and applicable permissions before adoption.

The distinction between program licensing and output licensing is also
described in [GNU's FAQ on program output](https://www.gnu.org/licenses/gpl-faq.en.html#WhatCaseIsOutputGPL).
The standard AGPL text in `LICENSE` remains unmodified.

## Optional attribution artwork

Attribution such as "Co-designed with eve.engineer" is appreciated where
practicable, but never required. It creates no publication, licensing, or
continued-use requirement for a design.

The original artwork, geometry data, KiCad footprint, FreeCAD sketch, and
accompanying scripts under `assets/branding/hardware/` are offered under
**CC0-1.0**, independently of Eve's application license. You may use and adapt
these assets in private, proprietary, commercial, and open-source designs.
Including the mark does not license your design under AGPL. This dedication
does not grant trademark rights or imply endorsement. See that directory's
`LICENSE` for the CC0 legal text.
