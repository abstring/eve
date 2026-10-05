"""Read-only design inventory and Git context."""

import hashlib
import os
import subprocess
from pathlib import Path

DESIGN_SUFFIXES = {
    ".kicad_pro", ".kicad_pcb", ".kicad_sch", ".kicad_dru",
    ".kicad_sym", ".kicad_mod",
}
SKIP_DIRS = {".git", ".eve", ".venv", "__pycache__", "node_modules"}


def project_root(path: Path) -> Path:
    root = path.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"Project root must be a directory: {root}")
    return root


def inventory(root: Path) -> dict[str, str]:
    files = {}
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (Path(directory) / d).is_symlink())
        for name in sorted(names):
            path = Path(directory) / name
            if path.suffix not in DESIGN_SUFFIXES and name not in {"sym-lib-table", "fp-lib-table"}:
                continue
            if path.is_symlink():
                raise ValueError(f"Symlinked design input is unsupported: {path}")
            files[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(files.items()))


def git_context(root: Path) -> dict:
    def git(*args: str):
        return subprocess.run(
            ["git", "--no-optional-locks", "-C", str(root), *args],
            capture_output=True, text=True, timeout=10, check=False,
        )
    try:
        top = git("rev-parse", "--show-toplevel")
        if top.returncode:
            return {"available": False, "reason": "not a Git checkout"}
        head = git("rev-parse", "--verify", "HEAD")
        status = git("status", "--porcelain=v1", "--untracked-files=normal")
        if status.returncode:
            raise RuntimeError(status.stderr.strip())
        return {
            "available": True, "root": top.stdout.strip(),
            "head": head.stdout.strip() if head.returncode == 0 else None,
            "dirty": bool(status.stdout), "status": status.stdout.splitlines(),
        }
    except FileNotFoundError:
        return {"available": False, "reason": "git is not installed"}


def inspect_project(root: Path) -> dict:
    return {"schema_version": 1, "root": str(root), "git": git_context(root), "files": inventory(root)}
