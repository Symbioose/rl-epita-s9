"""Sélectionne des traces réelles et décrit les erreurs observables, sans inventer de cause."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import read_jsonl


def analyze(root="artifacts/eval/test", output="results/ECHECS.md"):
    lines = ["# Analyse de traces réelles", "",
        "Sélection déterministe : trois échecs par condition au maximum, triés par identifiant de jeu.",
        "Une action non admissible ne suffit pas à conclure à une hallucination.", ""]
    found = False
    for folder in sorted(Path(root).iterdir() if Path(root).exists() else []):
        episodes_path = folder / "episodes.jsonl"
        if not (folder / "summary.json").exists() or not episodes_path.exists():
            continue
        summary = json.loads((folder / "summary.json").read_text())
        if not summary.get("complete"):
            continue
        failures = sorted([e for e in read_jsonl(episodes_path) if not e["won"]],
                          key=lambda e:e["game_id"])[:3]
        for episode in failures:
            trace = read_jsonl(folder / "traces" / f"{episode['game_id']}.jsonl")
            found = True
            lines += [f"## {folder.name} — {episode['game_id']}", "",
                f"Coups : {episode['steps']}. Non admissibles : {episode['invalid']}. "
                f"Revisite détectée : {episode['loop']}. Limite atteinte : {episode['truncated']}.", ""]
            if trace:
                lines += ["Objectif public :", "", trace[0]["observation"]["objective"], ""]
            first = next((i for i,t in enumerate(trace) if t["invalid"]), None)
            if first is not None:
                t = trace[first]
                lines += [f"Première commande non admissible au coup {first+1} : `{t['action']}`.",
                    "", "Description visible :", "", t["observation"]["description"], ""]
                if first+1 < len(trace):
                    lines += ["Réponse du jeu :", "", trace[first+1]["observation"]["feedback"], ""]
            lines += ["Séquence exécutée :", "", "```text",
                      *[f"{t['step']+1:02d}. {t['action']}" for t in trace], "```", ""]
    if not found:
        lines += ["Aucun échec réel issu d'une condition complète n'est disponible."]
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text("\n".join(lines)+"\n", encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="artifacts/eval/test")
    p.add_argument("--output", default="results/ECHECS.md")
    analyze(**vars(p.parse_args()))
