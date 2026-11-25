"""Exécution distante explicite. Aucune clé dans ce fichier.

modal run modal_app.py --phase prepare
modal run modal_app.py --phase train
modal run modal_app.py --phase validation
modal run modal_app.py --phase test
modal volume get textgames-student /artifacts ./artifacts

Les phases GPU séparées sont plafonnées à 30 minutes, la phase all à deux heures.
La préparation CPU est plafonnée à une heure. Aucun retry automatique.
Un timeout interrompt l'expérience : ne pas présenter des résultats partiels comme finaux.
"""
from pathlib import Path
import tomllib
import modal

app = modal.App("textgames-student")
volume = modal.Volume.from_name("textgames-student", create_if_missing=True)
project_file = Path(__file__).with_name("pyproject.toml") if modal.is_local() else Path("/project/pyproject.toml")
requirements = tomllib.loads(project_file.read_text())["project"]["dependencies"]
image = (modal.Image.debian_slim(python_version="3.11")
    .apt_install("build-essential", "git", "curl", "libffi-dev")
    # Installer les dépendances avant le code permet de réutiliser cette couche.
    .pip_install(*requirements)
    .add_local_file("pyproject.toml", "/project/pyproject.toml", copy=True)
    .add_local_dir("src", "/project/src", copy=True, ignore=["**/__pycache__/**", "**/*.pyc"])
    .run_commands("pip install --no-deps /project")
    .add_local_dir("scripts", "/project/scripts", copy=True, ignore=["**/__pycache__/**", "**/*.pyc"])
    .add_local_dir("tests", "/project/tests", copy=True, ignore=["**/__pycache__/**", "**/*.pyc"])
    .add_local_dir("presentation", "/project/presentation", copy=True, ignore=["**/__pycache__/**", "**/*.pyc"])
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


@app.function(image=image, volumes={"/storage": volume}, timeout=3600, retries=0,
              max_containers=1, cpu=2, memory=4096)
def prepare(scale: float):
    execute("prepare", scale)


@app.function(image=image, volumes={"/storage": volume}, timeout=300, retries=0,
              max_containers=1, cpu=2, memory=4096)
def verify():
    """Vérification Linux autonome, sans GPU ni modification des jeux."""
    import hashlib
    import subprocess
    import sys
    from textgame.common import save_json
    folder = Path("/storage/artifacts")
    folder.mkdir(exist_ok=True)
    result = subprocess.run(["python", "-m", "unittest", "discover", "-s", "/project/tests", "-v"],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (folder / "tests-final.log").write_text(result.stdout)
    complete = result.returncode == 0 and "skipped=" not in result.stdout
    save_json(folder / "tests-final.json", dict(complete=complete, exit_code=result.returncode,
        python=sys.version, source_sha256={str(p.relative_to("/project")):
        hashlib.sha256(p.read_bytes()).hexdigest() for base in ["src", "tests"]
        for p in Path("/project", base).rglob("*.py")}))
    volume.commit()
    print(result.stdout, flush=True)
    if not complete:
        raise RuntimeError("Les tests Linux n'ont pas tous été exécutés avec succès")


@app.function(image=image, volumes={"/storage": volume}, gpu="T4", timeout=1800,
              retries=0, max_containers=1, cpu=2, memory=8192)
def gpu_phase(phase: str, experiment: str = "", level: str = ""):
    execute(phase, 1, experiment, level)


@app.function(image=image, volumes={"/storage": volume}, gpu="T4", timeout=7200,
              retries=0, max_containers=1, cpu=2, memory=8192)
def full_project():
    import os
    import subprocess
    os.chdir("/storage")
    try:
        subprocess.run(["python", "/project/scripts/finish_project.py"], check=True)
    finally:
        volume.commit()


@app.local_entrypoint()
def main(phase: str = "prepare", scale: float = 1.0, experiment: str = "", level: str = ""):
    if phase not in {"all", "verify", "prepare", "train", "validation", "test"}:
        raise ValueError("Phase inconnue")
    if not 0 < scale <= 1:
        raise ValueError("scale doit appartenir à ]0,1]")
    if phase == "verify":
        verify.remote()
    elif phase == "all":
        if scale != 1 or experiment or level:
            raise ValueError("La phase all exécute le protocole complet uniquement")
        full_project.remote()
    elif phase == "prepare":
        prepare.remote(scale)
    else:
        gpu_phase.remote(phase, experiment, level)
