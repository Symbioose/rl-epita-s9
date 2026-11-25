"""Statistiques des démonstrations réellement collectées, au niveau des jeux."""
from collections import Counter
from pathlib import Path
import argparse
import json
import statistics
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import read_jsonl, save_json
from textgame.games import validate_manifest


def audit(root="artifacts", output="results/donnees.json"):
    root = Path(root)
    manifest = read_jsonl(root / "manifest.jsonl")
    validate_manifest(manifest)
    result = dict(games_by_level_split=dict(Counter(
        f"{g['level']}/{g['split']}" for g in manifest)), datasets={})
    collection = json.loads((root / "data" / "collection-report.json").read_text())
    rejected_ids = {g["game_id"] for g in collection["rejected_games"]}
    result["rejected_expert_games"] = collection["rejected_games"]
    for path in sorted((root / "data").glob("*.jsonl")):
        rows = read_jsonl(path)
        counts = Counter(r["game_id"] for r in rows)
        split = path.stem.rsplit("_", 1)[1]
        expected = {g["game_id"] for g in manifest if g["split"] == split and
                    (path.stem.startswith("mixed") or g["level"] == path.stem.split("_")[0])}
        if set(counts) != expected - rejected_ids:
            raise ValueError(f"Démonstrations incomplètes ou split incorrect : {path}")
        if not counts:
            raise ValueError(f"Aucune démonstration gagnante : {path}")
        result["datasets"][path.stem] = dict(examples=len(rows), games=len(counts),
            generated_games=len(expected), rejected_games=len(expected & rejected_ids),
            mean_expert_steps=statistics.mean(counts.values()),
            min_expert_steps=min(counts.values()), max_expert_steps=max(counts.values()),
            action_verbs=dict(Counter(r["action"].split()[0] for r in rows)))
    save_json(output, result)
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="artifacts")
    p.add_argument("--output", default="results/donnees.json")
    audit(**vars(p.parse_args()))
