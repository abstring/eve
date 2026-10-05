"""Run rules checks and retain evidence, without saving design changes."""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from eve.kicad import KiCadCLI
from eve.project import git_context, inventory, project_root


def verify(file: Path, root: Path, cli: KiCadCLI, timeout: float = 120) -> dict:
    root = project_root(root)
    raw = file.expanduser().absolute()
    # Reject symlink inputs instead of quietly verifying a different project.
    if raw.is_symlink():
        raise ValueError("Symlinked design input is unsupported")
    file = raw.resolve(strict=True)
    if not file.is_relative_to(root) or not file.is_file():
        raise ValueError("Design input must be a file within the project root")
    kinds = {".kicad_pcb": ("pcb", "drc"), ".kicad_sch": ("sch", "erc")}
    if file.suffix not in kinds:
        raise ValueError("Check expects a .kicad_pcb or .kicad_sch file")
    before = inventory(root)
    relative = str(file.relative_to(root))
    if relative not in before:
        raise ValueError("Design input is inside an excluded or symlinked directory")
    git_before = git_context(root)
    artifacts = root / ".eve"
    if artifacts.is_symlink() or (artifacts / "runs").is_symlink():
        raise ValueError("Artifact directories must not be symlinks")
    run = artifacts / "runs" / uuid4().hex
    run.mkdir(parents=True, exist_ok=False)
    report = run / "report.json"
    args = (*kinds[file.suffix], "--format", "json", "--severity-all",
            "--exit-code-violations", "--output", str(report), str(file))
    record = {
        "schema_version": 1, "started_at": datetime.now(timezone.utc).isoformat(),
        "input": relative, "inputs_before": before, "git": git_before,
        "kicad_version": cli.version, "command": [*cli.command, *args],
        "report": str(report), "manifest": str(run / "manifest.json"),
        "status": "tool_error", "returncode": None,
    }
    try:
        result = cli.run(*args, timeout=timeout)
        record.update(returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
        # KiCad uses 5 for rule violations; missing/malformed evidence never passes.
        if result.returncode in (0, 5):
            parsed = json.loads(report.read_text())
            expected_schema = f"https://schemas.kicad.org/{kinds[file.suffix][1]}.v1.json"
            if not isinstance(parsed, dict) or parsed.get("$schema") != expected_schema:
                raise ValueError("KiCad report has an unsupported schema identifier")
            groups = ("violations", "unconnected_items", "schematic_parity") if file.suffix == ".kicad_pcb" else ("sheets",)
            if any(not isinstance(parsed.get(group), list) for group in groups):
                raise ValueError("KiCad report is missing required result arrays")
            record["report_sha256"] = hashlib.sha256(report.read_bytes()).hexdigest()
            record["status"] = "passed" if result.returncode == 0 else "violations"
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        record["error"] = str(exc)
    try:
        after = inventory(root)
        record["inputs_after"] = after
        record["inputs_unchanged"] = before == after
    except (OSError, ValueError) as exc:
        record["inputs_unchanged"] = False
        record["error"] = str(exc)
    if not record["inputs_unchanged"]:
        record["status"] = "inputs_changed"
    record["finished_at"] = datetime.now(timezone.utc).isoformat()
    Path(record["manifest"]).write_text(json.dumps(record, indent=2) + "\n")
    return record
