"""Vrai test d'intégration, ignoré uniquement si TextWorld est absent."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


@unittest.skipUnless(importlib.util.find_spec("textworld"), "TextWorld non installé")
class TextWorldIntegration(unittest.TestCase):
    def test_compiled_game_has_text_and_oracle_wins(self):
        import textworld
        from textworld.generator import make_game, compile_game
        from textgame.games import start_game
        with tempfile.TemporaryDirectory() as folder:
            options = textworld.GameOptions()
            options.seeds = 1234
            options.nb_rooms = 2
            options.nb_objects = 3
            options.quest_length = 2
            options.path = str(Path(folder) / "game.ulx")
            game = make_game(options)
            path = compile_game(game, options)
            env = start_game(path, oracle=True)
            try:
                state = env.reset()
                self.assertTrue(state.description)
                self.assertTrue(state.objective)
                for _ in range(20):
                    self.assertTrue(state.policy_commands)
                    state, score, done = env.step(state.policy_commands[0])
                    if done:
                        break
                self.assertTrue(state.won)
            finally:
                env.close()
