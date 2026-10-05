"""Opt-in checks; temporary files live in Flatpak's accessible home."""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from eve.kicad import discover
from eve.verification import verify


@unittest.skipUnless(os.environ.get("EVE_LIVE_TESTS") == "1", "set EVE_LIVE_TESTS=1")
class LiveKiCadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eve-test-", dir=Path.home())
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for file in (Path(__file__).parent / "fixtures").iterdir():
            if file.is_file():
                shutil.copyfile(file, self.root / file.name)
        self.cli = discover()

    def test_outlined_board_passes(self):
        result = verify(self.root / "outlined.kicad_pcb", self.root, self.cli)
        self.assertEqual(result["status"], "passed", result)
        self.assertTrue(result["inputs_unchanged"])

    def test_missing_outline_fails(self):
        result = verify(self.root / "empty.kicad_pcb", self.root, self.cli)
        self.assertEqual(result["status"], "violations", result)
        self.assertTrue(result["inputs_unchanged"])

    def test_blank_schematic_passes(self):
        result = verify(self.root / "blank.kicad_sch", self.root, self.cli)
        self.assertEqual(result["status"], "passed", result)
        self.assertTrue(result["inputs_unchanged"])
