"""Behaviour cloning : historique public -> prochaine commande de l'expert."""
import argparse
from pathlib import Path
from .common import public_observation, read_jsonl, write_jsonl
from .games import start_game, validate_manifest


def collect(manifest="artifacts/manifest.jsonl", output="artifacts/data"):
    rows = read_jsonl(manifest)
    validate_manifest(rows)
    datasets = {}
    for game in rows:
        # Test réservé à l'évaluation : aucune démonstration test produite.
        if game["split"] == "test":
            continue
        env = start_game(game["path"], oracle=True)
        history, episode = [], []
        try:
            state = env.reset()
            for step in range(100):
                commands = state.get("policy_commands") or []
                if not commands:
                    break
                action = commands[0]
                observation = public_observation(state)
                episode.append(dict(game_id=game["game_id"], step=step,
                                    history=list(history), observation=observation, action=action))
                history.append(dict(observation=observation, action=action))
                state, score, done = env.step(action)
                if done:
                    break
            if not state.get("won"):
                raise RuntimeError(f"L'expert n'a pas gagné : {game['game_id']}")
            datasets.setdefault((game["level"], game["split"]), []).extend(episode)
        finally:
            env.close()
    for (level, split), examples in datasets.items():
        write_jsonl(Path(output) / f"{level}_{split}.jsonl", examples)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", default="artifacts/manifest.jsonl")
    p.add_argument("--output", default="artifacts/data")
    collect(**vars(p.parse_args()))
