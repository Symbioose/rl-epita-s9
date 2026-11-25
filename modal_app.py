"""Exécution distante explicite. Aucune clé dans ce fichier.

modal run modal_app.py --phase prepare
modal run modal_app.py --phase train
modal run modal_app.py --phase validation
modal run modal_app.py --phase test
modal volume get textgames-student /artifacts ./artifacts

Chaque appel GPU est plafonné à 30 minutes, sans retry automatique.
Un timeout interrompt l'expérience : ne pas présenter des résultats partiels comme finaux.
"""
from pathlib import Path
import modal

app = modal.App("textgames-student")
volume = modal.Volume.from_name("textgames-student", create_if_missing=True)
image = (modal.Image.debian_slim(python_version="3.11")
    .apt_install("build-essential", "git", "curl", "libffi-dev")
    .add_local_file("pyproject.toml", "/project/pyproject.toml", copy=True)
    .add_local_dir("src", "/project/src", copy=True)
    .run_commands("pip install /project")
    .add_local_dir("scripts", "/project/scripts", copy=True)
    .env({"HF_HOME": "/storage/hf", "PYTHONPATH": "/project/src"}))


def execute(phase, scale, experiment="", level=""):
    import os
    import subprocess
    os.chdir("/storage")
    extra = (["--experiment", experiment] if experiment else []) + (["--level", level] if level else [])
    try:
        subprocess.run(["python", "/project/scripts/run_experiments.py", "--phase", phase,
                        "--root", "artifacts", "--scale", str(scale)] + extra, check=True)
        if phase == "test":
            subprocess.run(["python", "/project/scripts/report.py", "--output",
                            "artifacts/rapport.md"], check=True)
    finally:
        volume.commit()


@app.function(image=image, volumes={"/storage": volume}, timeout=1800, retries=0,
              max_containers=1, cpu=2, memory=4096)
def prepare(scale: float):
    execute("prepare", scale)


@app.function(image=image, volumes={"/storage": volume}, gpu="T4", timeout=1800,
              retries=0, max_containers=1, cpu=2, memory=8192)
def gpu_phase(phase: str, experiment: str = "", level: str = ""):
    execute(phase, 1, experiment, level)


@app.local_entrypoint()
def main(phase: str = "prepare", scale: float = 1.0, experiment: str = "", level: str = ""):
    if phase not in {"prepare", "train", "validation", "test"}:
        raise ValueError("Phase inconnue")
    if not 0 < scale <= 1:
        raise ValueError("scale doit appartenir à ]0,1]")
    if phase == "prepare":
        prepare.remote(scale)
    else:
        gpu_phase.remote(phase, experiment, level)
