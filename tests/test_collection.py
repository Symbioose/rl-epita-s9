"""Une démonstration perdante ne doit jamais devenir une cible supervisée."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import read_jsonl, write_jsonl
from textgame.data import collect


class DemonstrationEnv:
    def __init__(self, wins):
        self.wins, self.closed = wins, False
    def reset(self):
        return dict(feedback="A key is here.", description="room", inventory="empty",
                    objective="take key", policy_commands=["take key"], won=False)
    def step(self, command):
        state = self.reset()
        state["won"] = self.wins
        return state, int(self.wins), self.wins
    def close(self):
        self.closed = True


class CollectionTests(unittest.TestCase):
    def test_reject_losing_episode_and_never_collect_test(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            manifest = root / "manifest.jsonl"
            write_jsonl(manifest, [dict(game_id=name, path=name, level="easy", split=split)
                for name, split in [("good", "train"), ("bad", "train"), ("unseen", "test")]])
            envs = []
            def factory(path, oracle):
                self.assertNotEqual(path, "unseen")
                self.assertTrue(oracle)
                env = DemonstrationEnv(path == "good")
                envs.append(env)
                return env
            with patch("textgame.data.validate_manifest"), patch("textgame.data.start_game", side_effect=factory), redirect_stdout(io.StringIO()):
                collect(str(manifest), str(root / "data"))
            rows = read_jsonl(root / "data/easy_train.jsonl")
            self.assertEqual({r["game_id"] for r in rows}, {"good"})
            report = json.loads((root / "data/collection-report.json").read_text())
            self.assertEqual(report["accepted_games"], ["good"])
            self.assertEqual(report["rejected_games"][0]["game_id"], "bad")
            self.assertEqual(report["test_demonstrations_collected"], 0)
            self.assertTrue(all(e.closed for e in envs))
            self.assertEqual(len(read_jsonl(root / "data/rejected/bad.jsonl")), 100)

    def test_execution_errors_are_not_silently_filtered(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "manifest.jsonl"
            write_jsonl(manifest, [dict(game_id="broken", path="broken", level="easy", split="train")])
            with patch("textgame.data.validate_manifest"), patch("textgame.data.start_game", side_effect=RuntimeError("backend error")):
                with self.assertRaisesRegex(RuntimeError, "backend error"):
                    collect(str(manifest), str(Path(folder) / "data"))
