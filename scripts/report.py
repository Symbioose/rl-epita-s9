"""Rapport produit uniquement à partir de rollouts terminés, jamais de valeurs fictives."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import read_jsonl


def report(root, output):
    rows = []
    for path in sorted(Path(root).glob("*/summary.json")):
        summary = json.loads(path.read_text())
        if not summary.get("complete"):
            continue
        m = summary["metrics"]
        lo, hi = m["success_ci95"]
        steps = "—" if m["mean_steps_success"] is None else f'{m["mean_steps_success"]:.1f}'
        rows.append(f'| {path.parent.name} | {m["n_games"]} | {m["success_rate"]:.1%} '
                    f'[{lo:.1%}, {hi:.1%}] | {m["mean_steps_all"]:.1f} | {steps} '
                    f'| {m["invalid_action_rate"]:.1%} | {m["loop_episode_rate"]:.1%} |')
    text = "# Résultats mesurés\n\n"
    if not rows:
        text += "Aucun rollout terminé disponible. Aucune performance de jeu mesurée.\n"
    else:
        text += ("IC Wilson à 95 % sur les jeux, une graine de fine-tuning.\n\n"
            "| Agent / niveau | Jeux | Réussite [IC 95 %] | Coups tous | Coups réussis | Invalides | Boucles |\n"
            "|---|---:|---:|---:|---:|---:|---:|\n" + "\n".join(rows) + "\n")
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="artifacts/eval/test")
    p.add_argument("--output", default="results/rapport.md")
    report(**vars(p.parse_args()))
