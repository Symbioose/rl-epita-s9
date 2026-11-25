"""Plan fixé avant le test. Usage : python scripts/run_experiments.py --phase prepare."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.games import generate
from textgame.data import collect
from textgame.train import train
from textgame.evaluate import evaluate
from textgame.common import read_jsonl, write_jsonl


def main(phase, root="artifacts", scale=1, epochs=3, experiment=None, level=None):
    if phase == "train" and experiment not in {None, "lora_easy", "lora_mixed"}:
        raise ValueError("Train accepte uniquement lora_easy ou lora_mixed")
    root = Path(root)
    manifest = str(root / "manifest.jsonl")
    if phase == "prepare":
        generate(root, scale)
        collect(manifest, str(root / "data"))
        # Même nombre d'époques, mais davantage d'exemples : comparaison adaptation,
        # pas comparaison à budget d'optimisation identique.
        for split in ["train", "validation"]:
            rows = sum([read_jsonl(root / "data" / f"{level}_{split}.jsonl")
                        for level in ["easy", "advanced"]], [])
            write_jsonl(root / "data" / f"mixed_{split}.jsonl", rows)
    elif phase == "train":
        for dataset in ["easy", "mixed"]:
            if experiment and experiment != "lora_" + dataset:
                continue
            train(str(root / "data" / f"{dataset}_train.jsonl"),
                  str(root / "data" / f"{dataset}_validation.jsonl"),
                  str(root / f"lora_{dataset}"), epochs=epochs)
    elif phase in ["validation", "test"]:
        # Une ablation d'inférence compare l'historique 0 / 4 pour le même modèle.
        for current_level in ([level] if level else ["easy", "advanced"]):
            for name, kind, adapter, history in [
                ("random", "random", None, 4), ("oracle", "oracle", None, 4),
                ("base", "model", None, 4),
                ("lora_easy", "model", str(root / "lora_easy"), 4),
                ("lora_easy_h0", "model", str(root / "lora_easy"), 0),
                ("lora_mixed", "model", str(root / "lora_mixed"), 4)]:
                if experiment and experiment != name:
                    continue
                evaluate(manifest, str(root / "eval" / phase / f"{name}_{current_level}"),
                         current_level, phase, kind, adapter, history, max_steps=30, seed=42)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--phase", required=True, choices=["prepare", "train", "validation", "test"])
    p.add_argument("--root", default="artifacts")
    p.add_argument("--scale", type=float, default=1)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--experiment", choices=["random", "oracle", "base", "lora_easy", "lora_easy_h0", "lora_mixed"])
    p.add_argument("--level", choices=["easy", "advanced"])
    main(**vars(p.parse_args()))
