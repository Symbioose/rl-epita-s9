"""Rejoue les démonstrations gagnantes pour exporter observation/action/récompense.

Ces fichiers illustrent le format RL. Le fine-tuning utilise les exemples SFT,
qui prédisent seulement la prochaine commande et n'optimisent pas la récompense.
"""
from collections import defaultdict
from pathlib import Path
import argparse
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import read_jsonl, write_jsonl, save_json, public_observation
from textgame.games import start_game, validate_manifest


def export(root="artifacts"):
    root = Path(root)
    manifest = read_jsonl(root / "manifest.jsonl")
    validate_manifest(manifest)
    games = {g["game_id"]:g for g in manifest}
    counts = {}
    for split in ["train", "validation"]:
        demonstrations = defaultdict(list)
        for level in ["easy", "advanced"]:
            for row in read_jsonl(root / "data" / f"{level}_{split}.jsonl"):
                demonstrations[row["game_id"]].append(row)
        transitions = []
        for game_id, examples in sorted(demonstrations.items()):
            game = games[game_id]
            assert game["split"] == split
            env = start_game(game["path"])
            try:
                state = env.reset()
                score = float(state.get("score") or 0)
                for example in sorted(examples, key=lambda r:r["step"]):
                    observation = public_observation(state)
                    state, new_score, done = env.step(example["action"])
                    transitions.append(dict(game_id=game_id, level=game["level"],
                        step=example["step"], observation=observation, action=example["action"],
                        reward=float(new_score)-score, score=float(new_score),
                        next_observation=public_observation(state), terminated=bool(done),
                        truncated=False, won=bool(state.get("won"))))
                    score = float(new_score)
                if not state.get("won"):
                    raise RuntimeError(f"La démonstration ne gagne pas à la réexécution : {game_id}")
            finally:
                env.close()
        write_jsonl(root / "transitions" / f"{split}.jsonl", transitions)
        counts[split] = dict(games=len(demonstrations), transitions=len(transitions))
        print(split, counts[split], flush=True)
    save_json(root / "transitions" / "verification.json", dict(
        all_demonstrations_replayed_and_won=True, splits=counts, test_replayed=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="artifacts")
    export(**vars(p.parse_args()))
