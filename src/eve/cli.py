"""Machine-readable CLI shared by humans and external agents."""

import argparse
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from eve import __version__
from eve.kicad import discover
from eve.project import inspect_project, project_root
from eve.verification import verify


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eve", description="Engineering tools for KiCad")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor", help="Inspect local KiCad capabilities")
    doctor.add_argument("--backend", choices=("auto", "native", "flatpak"), default="auto")
    inspect = sub.add_parser("inspect", help="Inventory design files and Git state")
    inspect.add_argument("root", type=Path, nargs="?", default=Path.cwd())
    check = sub.add_parser("check", help="Record an ERC or DRC check")
    check.add_argument("file", type=Path)
    check.add_argument("--project-root", type=Path, help="Defaults to the input file's directory")
    check.add_argument("--backend", choices=("auto", "native", "flatpak"), default="auto")
    check.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            result = {
                "schema_version": 1, "eve_version": __version__,
                "platform": platform.system(), "python": platform.python_version(),
                "git_available": shutil.which("git") is not None,
                "host_ipc_bindings_available": importlib.util.find_spec("kipy") is not None,
                "ipc_connection_tested": False,
            }
            try:
                cli = discover(args.backend)
                result["kicad"] = {"available": True, "version": cli.version, "command": cli.command}
                code = 0
            except RuntimeError as exc:
                result["kicad"] = {"available": False, "error": str(exc)}
                code = 2
        elif args.command == "inspect":
            result = inspect_project(project_root(args.root))
            code = 0
        else:
            if args.timeout <= 0:
                raise ValueError("Timeout must be positive")
            file = args.file.expanduser().absolute()
            result = verify(file, args.project_root or file.parent, discover(args.backend), args.timeout)
            code = 0 if result["status"] == "passed" else 1 if result["status"] == "violations" else 2
        print(json.dumps(result, indent=2))
        return code
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"schema_version": 1, "status": "error", "error": str(exc)}))
        return 2
