"""Small, bounded subprocess adapter for native and Flatpak KiCad."""

import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class KiCadCLI:
    command: tuple[str, ...]
    version: str

    def run(self, *args: str, timeout: float = 120) -> subprocess.CompletedProcess:
        return subprocess.run(
            [*self.command, *args], capture_output=True, text=True, timeout=timeout,
            check=False,
        )


def discover(backend: str = "auto") -> KiCadCLI:
    candidates = []
    native = shutil.which("kicad-cli")
    flatpak = shutil.which("flatpak")
    if native and backend in ("auto", "native"):
        candidates.append((native,))
    if flatpak and backend in ("auto", "flatpak"):
        candidates.append((flatpak, "run", "--command=kicad-cli", "org.kicad.KiCad"))
    for command in candidates:
        try:
            result = KiCadCLI(command, "").run("version", timeout=15)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode == 0 and result.stdout.strip():
            return KiCadCLI(command, result.stdout.strip())
    raise RuntimeError(
        f"No working {backend} KiCad CLI found. Install KiCad 9+ through your "
        "Linux distribution or org.kicad.KiCad through Flatpak."
    )
