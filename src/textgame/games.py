"""Génération reproductible. Compile en .ulx pour obtenir de vraies observations textuelles."""
import argparse
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


def generate(root="artifacts", scale=1):
    import textworld
    from textworld.generator import GameOptions
    root = Path(root)
    rows = []
    for level_index, (level, settings) in enumerate(LEVELS.items()):
        for split, (start, count) in SPLITS.items():
            for index in range(max(1, round(count * scale))):
                seed = level_index * 100000 + start + index
                options = GameOptions()
                options.seeds = seed
                for key, value in settings.items():
                    setattr(options, key, value)
                game = textworld.generator.make_game(options)
                path = root / "games" / level / split / f"{seed}.ulx"
                path.parent.mkdir(parents=True, exist_ok=True)
                options.path = str(path)
                textworld.generator.compile_game(game, options)
                rows.append(dict(game_id=f"{level}-{seed}", level=level, split=split,
                                 seed=seed, path=str(path), sha256=digest(path), **settings))
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
    args = parser.parse_args()
    if not 0 < args.scale <= 1:
        parser.error("scale doit appartenir à ]0,1]")
    generate(args.root, args.scale)
