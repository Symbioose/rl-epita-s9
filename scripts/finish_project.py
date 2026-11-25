"""Exécute le protocole complet. S'arrête dès la première erreur.

Nécessite l'installation de pyproject.toml et un accès aux poids Hugging Face.
Les étapes ne sont marquées terminées qu'après leur retour sans erreur.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from textgame.common import save_json, digest
from textgame.games import validate_manifest
from textgame.common import read_jsonl


def completed_training(root, name):
    folder = root / f"lora_{name}"
    metadata = folder / "training.json"
    if not metadata.exists() or not (folder / "adapter_model.safetensors").exists():
        return False
    info = json.loads(metadata.read_text())
    return (info["train_sha256"] == digest(root / "data" / f"{name}_train.jsonl")
            and info["validation_sha256"] == digest(root / "data" / f"{name}_validation.jsonl")
            and info["epochs"] == 3 and info["max_steps"] == -1 and info["seed"] == 42)


def main(root="artifacts"):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    ledger = []

    def run(label, command):
        begin = time.time()
        logfile = root / "execution" / f"{len(ledger):02}-{label}.log"
        logfile.parent.mkdir(exist_ok=True)
        print(f"[{label}] En cours ; journal : {logfile}", flush=True)
        with logfile.open("w") as stream:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
        ledger.append(dict(step=label, returncode=result.returncode,
                           seconds=time.time()-begin, log=str(logfile)))
        save_json(root / "execution.json", ledger)
        if result.returncode:
            raise RuntimeError(f"Étape {label} échouée : consulter {logfile}")

    missing = [m for m in ["textworld", "torch", "transformers", "peft", "accelerate"]
               if importlib.util.find_spec(m) is None]
    if missing:
        save_json(root / "blocked.json", dict(reason="missing_dependencies", packages=missing))
        raise RuntimeError("Dépendances absentes : " + ", ".join(missing))
    run("tests", [sys.executable, "-m", "unittest", "discover", "-s", str(PROJECT / "tests"), "-v"])
    script = str(PROJECT / "scripts" / "run_experiments.py")
    common = [sys.executable, script, "--root", str(root)]
    if (root / "manifest.jsonl").exists():
        validate_manifest(read_jsonl(root / "manifest.jsonl"))
        # Un manifeste de smoke-test ne doit jamais servir au rendu final.
        from textgame.games import SPLITS
        games = read_jsonl(root / "manifest.jsonl")
        for level in ["easy", "advanced"]:
            for split, (_, expected) in SPLITS.items():
                if sum(g["level"] == level and g["split"] == split for g in games) != expected:
                    raise ValueError("Manifeste réduit : utiliser un nouveau root pour le protocole complet")
        # Recollecter les démonstrations si la préparation a été interrompue.
        from textgame.data import collect
        from textgame.common import write_jsonl
        collect(str(root / "manifest.jsonl"), str(root / "data"))
        for split in ["train", "validation"]:
            write_jsonl(root / "data" / f"mixed_{split}.jsonl",
                        read_jsonl(root / "data" / f"easy_{split}.jsonl") +
                        read_jsonl(root / "data" / f"advanced_{split}.jsonl"))
    else:
        run("prepare", common + ["--phase", "prepare"])
    for dataset in ["easy", "mixed"]:
        if not completed_training(root, dataset):
            run(f"train-{dataset}", common + ["--phase", "train", "--experiment", f"lora_{dataset}"])
    # Protocole fixé : aucun réglage automatique après consultation du test.
    for split in ["validation", "test"]:
        for level in ["easy", "advanced"]:
            for agent in ["oracle", "random", "base", "lora_easy", "lora_easy_h0", "lora_mixed"]:
                run(f"{split}-{agent}-{level}", common + ["--phase", split,
                    "--experiment", agent, "--level", level])
    delivery = root / "delivery"
    delivery.mkdir(exist_ok=True)
    run("report", [sys.executable, str(PROJECT / "scripts/report.py"), "--root",
                   str(root / "eval/test"), "--output", str(delivery / "resultats.md")])
    run("slides", [sys.executable, str(PROJECT / "presentation/build.py"), "--results",
                   str(root / "eval/test"), "--output", str(delivery)])
    save_json(delivery / "completion.json", dict(complete=True,
        manifest_sha256=digest(root / "manifest.jsonl"), evaluation_conditions=12,
        description="Deux niveaux, six agents, validation puis test ; résultats dans les logs."))
    print(f"Protocole terminé. Rendus : {delivery}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="artifacts")
    main(**vars(parser.parse_args()))
