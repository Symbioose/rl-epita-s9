"""Un arrêt du calcul ne doit pas produire une réussite expérimentale fictive."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import digest, write_jsonl, save_json
from textgame.evaluate import evaluate


class ResumeTests(unittest.TestCase):
    def test_resume_only_pending_games_and_reject_changed_config(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            games = []
            for i in range(2):
                path = root / f"{i}.z8"
                path.write_text(str(i))
                games.append(dict(game_id=str(i), seed=i, sha256=digest(path), path=str(path),
                                  level="easy", split="test"))
            manifest, output = root / "manifest.jsonl", root / "eval"
            write_jsonl(manifest, games)
            def win(game, *args):
                return dict(game_id=game["game_id"], won=True, steps=2, invalid=0,
                            loop=False, truncated=False), []
            calls = []
            def interrupted(game, *args):
                calls.append(game["game_id"])
                if len(calls) == 2:
                    raise RuntimeError("interruption simulée")
                return win(game)
            with patch("textgame.evaluate.rollout", side_effect=interrupted):
                with self.assertRaises(RuntimeError):
                    evaluate(str(manifest), str(output), kind="oracle")
            self.assertFalse((output / "summary.json").exists())
            with patch("textgame.evaluate.rollout", side_effect=win) as rolled:
                result = evaluate(str(manifest), str(output), kind="oracle")
            self.assertEqual(rolled.call_count, 1)
            self.assertEqual(result["n_games"], 2)
            self.assertTrue(json.loads((output / "summary.json").read_text())["complete"])
            with self.assertRaises(ValueError):
                evaluate(str(manifest), str(output), kind="oracle", max_steps=31)
            # Une exécution finie n'a pas besoin de recharger un modèle ni de rejouer.
            with patch("textgame.evaluate.rollout", side_effect=AssertionError("ne pas rejouer")):
                self.assertEqual(evaluate(str(manifest), str(output), kind="oracle")["successes"], 2)

    def test_output_without_provenance_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "game.z8"
            path.write_text("game")
            manifest = root / "manifest.jsonl"
            write_jsonl(manifest, [dict(game_id="one", seed=1, sha256=digest(path), path=str(path),
                                       level="easy", split="test")])
            output = root / "eval"
            save_json(output / "summary.json", dict(metrics={}))
            with self.assertRaises(ValueError):
                evaluate(str(manifest), str(output), kind="oracle")
