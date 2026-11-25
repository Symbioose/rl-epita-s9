"""Tests des garanties scientifiques, sans téléchargement de modèle."""
import json
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import messages, public_observation, digest, normalize_action
from textgame.games import validate_manifest
from textgame.tokenization import encode_example, pad_examples
from textgame.evaluate import summarize, wilson, rollout


class ToyTokenizer:
    """Template simplifié pour tester les masques, pas un modèle de remplacement."""
    def apply_chat_template(self, messages, tokenize, add_generation_prompt):
        text = "".join(f"<{m['role']}>{m['content']}!" for m in messages)
        if add_generation_prompt:
            text += "<assistant>"
        return list(text.encode())


class TinyEnv:
    def __init__(self):
        self.closed = False
    def reset(self):
        return dict(feedback="A key lies here.", description="room", inventory="empty",
                    objective="take key", policy_commands=["take key"],
                    admissible_commands=["take key"], score=0)
    def step(self, action):
        state = self.reset()
        state.update(won=action == "take key", score=int(action == "take key"))
        return state, state["score"], state["won"]
    def close(self):
        self.closed = True


class PipelineTests(unittest.TestCase):
    def test_observation_whitelist(self):
        obs = public_observation(dict(feedback="visible", policy_commands=["SECRET"], facts=["HIDDEN"]))
        self.assertNotIn("SECRET", json.dumps(messages([], obs)))
        self.assertEqual(set(obs), {"feedback", "description", "inventory", "objective"})

    def test_history_zero_and_four(self):
        history = [dict(observation={"feedback": str(i)}, action=str(i)) for i in range(8)]
        self.assertEqual(len(messages(history, {}, 0)), 2)
        self.assertEqual(len(messages(history, {}, 4)), 10)
        self.assertEqual(history[0]["action"], "0")

    def test_action_only_loss(self):
        row = dict(history=[], observation={}, action="take key")
        e = encode_example(ToyTokenizer(), row)
        target = bytes(x for x in e["labels"] if x != -100).decode()
        self.assertEqual(target, "take key!")
        self.assertEqual(e["labels"][0], -100)

    def test_padding_never_contributes_to_loss(self):
        rows = [dict(input_ids=[1, 2], attention_mask=[1, 1], labels=[-100, 2]),
                dict(input_ids=[1], attention_mask=[1], labels=[1])]
        batch = pad_examples(rows, 99)
        self.assertEqual(batch["labels"][1], [1, -100])
        self.assertEqual(batch["attention_mask"][1], [1, 0])

    def test_long_observation_fails_explicitly(self):
        with self.assertRaises(ValueError):
            encode_example(ToyTokenizer(), dict(history=[], observation={}, action="go"), max_length=2)

    def test_duplicate_games_and_modified_games(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "game.ulx"
            p.write_bytes(b"test")
            row = dict(path=str(p), sha256=digest(p), seed=10)
            validate_manifest([row])
            with self.assertRaises(ValueError):
                validate_manifest([row, row])
            p.write_bytes(b"changed")
            with self.assertRaises(ValueError):
                validate_manifest([row])

    def test_wilson_boundaries(self):
        self.assertIsNone(wilson(0, 0))
        self.assertAlmostEqual(wilson(0, 40)[0], 0)
        self.assertGreater(wilson(0, 40)[1], 0)
        self.assertLess(wilson(40, 40)[0], 1)

    def test_metrics_weight_invalid_by_actions(self):
        episodes = [dict(won=True, steps=2, invalid=0, loop=False, truncated=False),
                    dict(won=False, steps=30, invalid=8, loop=True, truncated=True)]
        result = summarize(episodes)
        self.assertEqual(result["invalid_action_rate"], 8/32)
        self.assertEqual(result["mean_steps_success"], 2)
        self.assertEqual(result["mean_steps_all"], 16)
        self.assertIsNone(summarize(episodes[1:])["mean_steps_success"])

    def test_model_never_receives_oracle_or_candidates(self):
        env = TinyEnv()
        class Agent:
            def act(self, history, observation):
                assert "policy_commands" not in observation
                assert "admissible_commands" not in observation
                return "take key"
        result, trace = rollout(dict(path="fake", game_id="fake", level="easy"), Agent(),
                                env_factory=lambda *a, **k: env)
        self.assertTrue(result["won"])
        self.assertEqual(trace[0]["reward"], 1)
        self.assertTrue(env.closed)

    def test_loop_and_truncation(self):
        class Agent:
            def act(self, *args):
                return "dance"
        result, trace = rollout(dict(path="fake", game_id="fake", level="easy"), Agent(),
                                max_steps=4, env_factory=lambda *a, **k: TinyEnv())
        self.assertEqual(result["invalid"], 4)
        self.assertTrue(result["loop"])
        self.assertTrue(result["truncated"])

    def test_empty_generation(self):
        self.assertEqual(normalize_action("\n  "), "")
        self.assertEqual(normalize_action("take key\nExplanation"), "take key")


if __name__ == "__main__":
    unittest.main()
