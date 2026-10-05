import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from eve.kicad import KiCadCLI, discover
from eve.project import git_context, inventory
from eve.verification import verify


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.board = self.root / "board with spaces.kicad_pcb"
        self.board.write_text("test design")
        self.cli = KiCadCLI(("kicad-cli",), "10.0.6")

    def run_check(self, code=0, content=None, mutate=False):
        def fake(*args, **kwargs):
            report = Path(args[args.index("--output") + 1])
            report.write_text(json.dumps(content if content is not None else {
                "$schema": "https://schemas.kicad.org/drc.v1.json",
                "violations": [], "unconnected_items": [], "schematic_parity": [],
            }))
            if mutate:
                self.board.write_text("changed by tool")
            return subprocess.CompletedProcess(args, code, "tool output", "")
        with patch.object(KiCadCLI, "run", side_effect=fake):
            return verify(self.board, self.root, self.cli)

    def test_pass_keeps_input_and_records_evidence(self):
        result = self.run_check()
        self.assertEqual(result["status"], "passed")
        self.assertTrue(result["inputs_unchanged"])
        self.assertEqual(self.board.read_text(), "test design")
        self.assertEqual(result["command"][-1], str(self.board))
        self.assertNotIn("--save-board", result["command"])
        self.assertNotIn("--refill-zones", result["command"])
        self.assertEqual(json.loads(Path(result["manifest"]).read_text()), result)

    def test_rule_violations_are_distinct_from_tool_failure(self):
        self.assertEqual(self.run_check(code=5)["status"], "violations")
        self.assertEqual(self.run_check(code=3)["status"], "tool_error")

    def test_bad_report_never_passes(self):
        self.assertEqual(self.run_check(content={"unexpected": []})["status"], "tool_error")

    def test_missing_result_arrays_never_passes(self):
        result = self.run_check(content={"$schema": "https://schemas.kicad.org/drc.v1.json"})
        self.assertEqual(result["status"], "tool_error")

    def test_changed_inputs_invalidate_result(self):
        self.assertEqual(self.run_check(mutate=True)["status"], "inputs_changed")

    def test_timeout_preserves_manifest(self):
        with patch.object(KiCadCLI, "run", side_effect=subprocess.TimeoutExpired("kicad", 1)):
            result = verify(self.board, self.root, self.cli)
        self.assertEqual(result["status"], "tool_error")
        self.assertTrue(Path(result["manifest"]).exists())

    def test_missing_report_never_passes(self):
        with patch.object(KiCadCLI, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
            result = verify(self.board, self.root, self.cli)
        self.assertEqual(result["status"], "tool_error")

    def test_runs_do_not_overwrite(self):
        self.assertNotEqual(self.run_check()["report"], self.run_check()["report"])

    def test_outside_input_and_wrong_type_rejected(self):
        (self.root / "nested").mkdir()
        with self.assertRaises(ValueError):
            verify(self.board, self.root / "nested", self.cli)
        readme = self.root / "README.md"
        readme.write_text("not a board")
        with self.assertRaises(ValueError):
            verify(readme, self.root, self.cli)

    def test_symlinked_artifacts_rejected(self):
        target = self.root / "elsewhere"
        target.mkdir()
        (self.root / ".eve").symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            verify(self.board, self.root, self.cli)

    def test_inventory_skips_artifacts_and_rejects_linked_designs(self):
        hidden = self.root / ".eve"
        hidden.mkdir()
        (hidden / "ignored.kicad_pcb").write_text("artifact")
        self.assertEqual(list(inventory(self.root)), [self.board.name])
        (self.root / "link.kicad_pcb").symlink_to(self.board)
        with self.assertRaises(ValueError):
            inventory(self.root)

    def test_dirty_git_state_is_recorded_without_modification(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        context = git_context(self.root)
        self.assertTrue(context["available"])
        self.assertTrue(context["dirty"])
        self.assertIsNone(context["head"])


class DiscoveryTests(unittest.TestCase):
    def test_falls_back_to_flatpak(self):
        results = [subprocess.CompletedProcess([], 1, "", "broken native"),
                   subprocess.CompletedProcess([], 0, "10.0.6\n", "")]
        with patch("eve.kicad.shutil.which", side_effect=lambda name: "/usr/bin/" + name):
            with patch.object(KiCadCLI, "run", side_effect=results):
                cli = discover()
        self.assertEqual(cli.command[-1], "org.kicad.KiCad")
        self.assertEqual(cli.version, "10.0.6")

    def test_explicit_backend_does_not_silently_switch(self):
        with patch("eve.kicad.shutil.which", return_value=None):
            with self.assertRaises(RuntimeError):
                discover("native")


if __name__ == "__main__":
    unittest.main()
