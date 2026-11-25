"""Archive les artefacts vérifiés ; aucun poids du modèle de base ni secret."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import tarfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.common import read_jsonl, save_json, digest
from textgame.games import validate_manifest
from textgame.evaluate import METRICS_VERSION

AGENTS = ["oracle", "random", "base", "lora_easy", "lora_easy_h0", "lora_mixed"]


def package(root="artifacts", output="reproducibility/experiences.tar.gz"):
    root, output = Path(root), Path(output)
    manifest = read_jsonl(root / "manifest.jsonl")
    validate_manifest(manifest)
    verified = json.loads((root / "tests-final.json").read_text())
    if not verified["complete"]:
        raise ValueError("Vérification Linux complète requise")
    for split in ["validation", "test"]:
        for level in ["easy", "advanced"]:
            expected = sum(g["split"] == split and g["level"] == level for g in manifest)
            for name in AGENTS:
                folder = root / "eval" / split / f"{name}_{level}"
                summary = json.loads((folder / "summary.json").read_text())
                if not summary.get("complete") or summary["metrics"]["n_games"] != expected:
                    raise ValueError(f"Évaluation incomplète : {folder}")
                if summary["config"]["manifest_sha256"] != digest(root / "manifest.jsonl"):
                    raise ValueError(f"Manifeste différent : {folder}")
                if name.startswith("lora_"):
                    model_name = "lora_easy" if name == "lora_easy_h0" else name
                    if summary["config"]["adapter_sha256"] != digest(root / model_name / "adapter_model.safetensors"):
                        raise ValueError(f"Poids différents : {folder}")
                if summary["config"].get("metrics_version") != METRICS_VERSION:
                    raise ValueError("Recalculer les diagnostics avec recompute_metrics.py")
    models = {}
    for name in ["lora_easy", "lora_mixed"]:
        folder = root / name
        info = json.loads((folder / "training.json").read_text())
        dataset = name.removeprefix("lora_")
        for split in ["train", "validation"]:
            if info[f"{split}_sha256"] != digest(root / "data" / f"{dataset}_{split}.jsonl"):
                raise ValueError(f"Les données ne correspondent pas au modèle : {name}, {split}")
        models[name] = dict(base_model=info["model"], base_revision=info["base_commit"],
                           adapter_sha256=digest(folder / "adapter_model.safetensors"))
    allowed = ["games", "data", "transitions", "lora_easy", "lora_mixed", "eval",
               "execution", "execution.json", "delivery", "manifest.jsonl", "tests-final.log", "tests-final.json"]
    files = []
    for name in allowed:
        base = root / name
        candidates = base.rglob("*") if base.is_dir() else [base]
        files.extend(p for p in candidates if p.is_file() and "checkpoints" not in p.parts
                     and not p.name.startswith(".") and not p.name.endswith((".tmp", ".lock")))
    output.parent.mkdir(parents=True, exist_ok=True)
    def normalized_header(info):
        info.uid = info.gid = 0
        info.uname = info.gname = ""
        info.mtime = 0
        return info
    # mtime=0 et ordre stable : une archive identique pour des fichiers identiques.
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", compresslevel=9, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for path in sorted(files):
                    archive.add(path, arcname=str(Path("artifacts") / path.relative_to(root)),
                                filter=normalized_header)
    if output.stat().st_size > 90_000_000:
        raise ValueError("Archive trop volumineuse pour une publication GitHub directe")
    checksum = digest(output)
    output.with_suffix(output.suffix + ".sha256").write_text(f"{checksum}  {output.name}\n")
    save_json(output.with_name("manifest.json"), dict(archive=output.name, sha256=checksum,
        bytes=output.stat().st_size, files=len(files), games=len(manifest), models=models,
        complete_evaluation_conditions=24, metrics_version=METRICS_VERSION))
    print(f"Archive vérifiée : {output} ({output.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="artifacts")
    p.add_argument("--output", default="reproducibility/experiences.tar.gz")
    package(**vars(p.parse_args()))
