"""Génération reproductible. Compile en .z8 pour obtenir de vraies observations textuelles."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from .common import digest, read_jsonl, write_jsonl

LEVELS = {"easy": dict(nb_rooms=3, nb_objects=5, quest_length=3, quest_breadth=1),
          "advanced": dict(nb_rooms=6, nb_objects=10, quest_length=7, quest_breadth=2)}
SPLITS = {"train": (10000, 120), "validation": (20000, 20), "test": (30000, 40)}


def validate_manifest(rows):
    seeds = [r["seed"] for r in rows]
    hashes = [r["sha256"] for r in rows]
    if len(seeds) != len(set(seeds)) or len(hashes) != len(set(hashes)):
        raise ValueError("Jeux dupliqués ou graines partagées entre splits")
    for row in rows:
        if digest(row["path"]) != row["sha256"]:
            raise ValueError(f"Jeu modifié : {row['path']}")
        if row.get("game_json_sha256") and digest(Path(row["path"]).with_suffix(".json")) != row["game_json_sha256"]:
            raise ValueError(f"Métadonnées du jeu modifiées : {row['path']}")


def _valid_compiled_game(path):
    """Écarte notamment un binaire interrompu au milieu de sa compilation."""
    if not path.exists():
        return False
    content = path.read_bytes()
    if len(content) < 64 or content[0] != 8:
        return False
    length = int.from_bytes(content[26:28], "big") * 8
    checksum = int.from_bytes(content[28:30], "big")
    return 64 <= length <= len(content) and sum(content[64:length]) % 65536 == checksum


def _generate_one(job):
    import textworld
    from textworld.generator import GameOptions
    root, level, split, seed, settings = job
    options = GameOptions()
    options.seeds = seed
    for key, value in settings.items():
        setattr(options, key, value)
    path = Path(root) / "games" / level / split / f"{seed}.z8"
    path.parent.mkdir(parents=True, exist_ok=True)
    options.path = str(path)
    source = path.with_suffix(".json")
    cached = _valid_compiled_game(path) and source.exists()
    if cached:
        previous = textworld.Game.load(str(source))
        if previous.metadata.get("uuid") != options.uuid:
            raise ValueError(f"Jeu déjà présent avec d'autres paramètres : {path}")
    else:
        options.force_recompile = True
        game = textworld.generator.make_game(options)
        textworld.generator.compile_game(game, options)
        if not _valid_compiled_game(path):
            raise ValueError(f"Compilation incomplète : {path}")
    return dict(game_id=f"{level}-{seed}", level=level, split=split,
                seed=seed, path=str(path), sha256=digest(path),
                game_json_sha256=digest(source), **settings)


def generate(root="artifacts", scale=1, workers=2):
    if not 0 < scale <= 1 or workers < 1:
        raise ValueError("scale dans ]0,1], workers >= 1")
    root = Path(root)
    jobs = []
    for level_index, (level, settings) in enumerate(LEVELS.items()):
        for split, (start, count) in SPLITS.items():
            for index in range(max(1, round(count * scale))):
                seed = level_index * 100000 + start + index
                jobs.append((str(root), level, split, seed, settings))
    rows = []
    def record(row):
        rows.append(row)
        write_jsonl(root / "generation-progress.jsonl", sorted(rows, key=lambda r:r["seed"]))
        print(f"Génération : {len(rows)}/{len(jobs)} — {row['game_id']}", flush=True)
    if workers == 1:
        for job in jobs:
            record(_generate_one(job))
    else:
        # Processus CPU isolés : les RNG ne dépendent pas de l'ordre d'exécution.
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for future in as_completed([executor.submit(_generate_one, job) for job in jobs]):
                record(future.result())
    rows.sort(key=lambda r:r["seed"])
    validate_manifest(rows)
    write_jsonl(root / "manifest.jsonl", rows)
    return rows


def start_game(path, oracle=False):
    import textworld
    # Les commandes admissibles sont réservées aux métriques et baselines explicites.
    infos = textworld.EnvInfos(description=True, inventory=True, objective=True,
                              admissible_commands=True, won=True, lost=True,
                              score=True, max_score=True, policy_commands=oracle)
    return textworld.start(str(path), infos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="artifacts")
    parser.add_argument("--scale", type=float, default=1)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    if not 0 < args.scale <= 1:
        parser.error("scale doit appartenir à ]0,1]")
    generate(args.root, args.scale, args.workers)
