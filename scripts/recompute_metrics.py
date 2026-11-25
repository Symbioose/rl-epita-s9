"""Recalcule les diagnostics depuis les traces, sans rejouer le modèle.

La version 2 ignore le compteur de coups imprimé dans le feedback pour détecter
les revisites. Les victoires, commandes et nombres de coups restent inchangés.
"""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import read_jsonl, write_jsonl, save_json
from textgame.evaluate import loop_signature, summarize, METRICS_VERSION


def recompute(root="artifacts/eval", output="results/verification_metriques.json"):
    audit = []
    for run_path in sorted(Path(root).glob("*/*/run.json")):
        folder = run_path.parent
        summary_path = folder / "summary.json"
        summary = json.loads(summary_path.read_text()) if summary_path.exists() else None
        config = json.loads(run_path.read_text())
        episode_path = folder / "episodes.jsonl"
        episodes = read_jsonl(episode_path) if episode_path.exists() else []
        old_loops = sum(e["loop"] for e in episodes)
        for episode in episodes:
            trace = read_jsonl(folder / "traces" / f"{episode['game_id']}.jsonl")
            if len(trace) != episode["steps"]:
                raise ValueError(f"Trace incomplète : {episode['game_id']}")
            signatures = [loop_signature(t["observation"], t["action"]) for t in trace]
            episode["loop"] = len(signatures) != len(set(signatures))
        new = summarize(episodes) if episodes else None
        # Il s'agit d'une correction des diagnostics, jamais d'une sélection de parties.
        if summary and summary.get("complete"):
            for key in ["n_games", "successes", "success_rate", "mean_steps_all", "mean_steps_success", "invalid_action_rate"]:
                if new[key] != summary["metrics"][key]:
                    raise ValueError(f"Un résultat principal a changé : {folder}, {key}")
            summary["metrics"] = new
            summary["config"]["metrics_version"] = METRICS_VERSION
            save_json(summary_path, summary)
        config["metrics_version"] = METRICS_VERSION
        if episode_path.exists():
            write_jsonl(episode_path, episodes)
        save_json(run_path, config)
        audit.append(dict(condition=str(folder.relative_to(root)), games=len(episodes),
            old_loop_episodes=old_loops, corrected_loop_episodes=sum(e["loop"] for e in episodes),
            complete=bool(summary and summary.get("complete")), main_outcomes_unchanged=True))
    save_json(output, dict(metrics_version=METRICS_VERSION, conditions=audit))
    print(len(audit), "conditions vérifiées")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="artifacts/eval")
    p.add_argument("--output", default="results/verification_metriques.json")
    recompute(**vars(p.parse_args()))
