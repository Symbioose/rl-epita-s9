"""Rollouts, métriques au niveau des jeux et traces d'échec auditables."""
import argparse
import json
import hashlib
import math
import statistics
import time
from pathlib import Path
from .common import read_jsonl, write_jsonl, save_json, public_observation, digest
from .games import start_game, validate_manifest
from .agents import RandomAgent, LanguageAgent

METRICS_VERSION = 2


def loop_signature(observation, action):
    # Le feedback contient un compteur de coups qui change même lors d'un cycle.
    # Une revisite observable se mesure sur la pièce, l'inventaire et la commande.
    return (observation["description"], observation["inventory"], action.strip().casefold())


def wilson(successes, total):
    if not total:
        return None
    z = 1.959963984540054
    p, denominator = successes / total, 1 + z*z / total
    center = (p + z*z/(2*total)) / denominator
    margin = z * math.sqrt(p*(1-p)/total + z*z/(4*total*total)) / denominator
    return [max(0, center-margin), min(1, center+margin)]


def summarize(episodes):
    if not episodes:
        raise ValueError("Aucun épisode à évaluer")
    successes = [e for e in episodes if e["won"]]
    steps = sum(e["steps"] for e in episodes)
    return dict(n_games=len(episodes), successes=len(successes),
        success_rate=len(successes)/len(episodes),
        success_ci95=wilson(len(successes), len(episodes)),
        mean_steps_all=statistics.mean(e["steps"] for e in episodes),
        mean_steps_success=statistics.mean(e["steps"] for e in successes) if successes else None,
        invalid_action_rate=sum(e["invalid"] for e in episodes)/steps if steps else None,
        loop_episode_rate=sum(e["loop"] for e in episodes)/len(episodes),
        truncation_rate=sum(e["truncated"] for e in episodes)/len(episodes))


def rollout(game, agent, kind="model", max_steps=30, env_factory=start_game):
    env = env_factory(game["path"], oracle=kind == "oracle")
    trace, history, invalid = [], [], 0
    seen, loop, done = set(), False, False
    start = time.monotonic()
    try:
        state = env.reset()
        score = float(state.get("score") or 0)
        for step in range(max_steps):
            obs = public_observation(state)
            admissible = state.get("admissible_commands") or []
            if kind == "oracle":
                policy = state.get("policy_commands") or []
                action = policy[0] if policy else "look"
            elif kind == "random":
                action = agent.act(history, obs, admissible)
            else:
                action = agent.act(history, obs)
            # look / inventory sont des commandes valides mais non productives.
            normalized = action.strip().casefold()
            is_invalid = normalized not in {a.casefold() for a in admissible} and normalized not in {"look", "inventory"}
            invalid += int(is_invalid)
            signature = loop_signature(obs, action)
            loop |= signature in seen
            seen.add(signature)
            next_state, next_score, done = env.step(action)
            trace.append(dict(step=step, observation=obs, action=action,
                admissible_commands=admissible, invalid=is_invalid,
                reward=float(next_score)-score, score=float(next_score),
                won=bool(next_state.get("won"))))
            history.append(dict(observation=obs, action=action))
            state, score = next_state, float(next_score)
            if done:
                break
        episode = dict(game_id=game["game_id"], level=game["level"],
            won=bool(state.get("won")), lost=bool(state.get("lost")),
            steps=len(trace), invalid=invalid, loop=loop, truncated=not done,
            score=score, seconds=time.monotonic()-start)
        return episode, trace
    finally:
        env.close()


def evaluate(manifest="artifacts/manifest.jsonl", output="artifacts/eval/base_easy",
             level="easy", split="test", kind="model", adapter=None,
             history_size=4, max_steps=30, seed=42):
    games = read_jsonl(manifest)
    validate_manifest(games)
    selected = [g for g in games if g["level"] == level and g["split"] == split]
    if not selected:
        raise ValueError("Aucun jeu pour ce niveau et ce split")
    output = Path(output)
    config = dict(level=level, split=split, kind=kind, adapter=adapter,
                  history_size=history_size, max_steps=max_steps, seed=seed,
                  metrics_version=METRICS_VERSION,
                  manifest_sha256=digest(manifest))
    if adapter:
        weights = Path(adapter) / "adapter_model.safetensors"
        config["adapter_sha256"] = digest(weights)
    config_path = output / "run.json"
    if config_path.exists():
        if json.loads(config_path.read_text()) != config:
            raise ValueError("Le dossier contient une autre expérience : choisir un nouvel output")
    elif (output / "episodes.jsonl").exists() or (output / "summary.json").exists():
        raise ValueError("Résultats sans provenance : choisir un nouvel output")
    save_json(config_path, config)
    # Reprise uniquement avec même manifeste, mêmes poids et même configuration.
    episodes_path = output / "episodes.jsonl"
    episodes = read_jsonl(episodes_path) if episodes_path.exists() else []
    completed_ids = [e["game_id"] for e in episodes]
    if len(completed_ids) != len(set(completed_ids)) or not set(completed_ids) <= {g["game_id"] for g in selected}:
        raise ValueError("Épisodes incohérents avec le manifeste")
    summary_path = output / "summary.json"
    # Un résumé n'est publié qu'après complétion de TOUS les jeux sélectionnés.
    summary_path.unlink(missing_ok=True)
    if len(episodes) == len(selected):
        save_json(summary_path, dict(config=config, complete=True, metrics=summarize(episodes)))
        return summarize(episodes)
    agent = RandomAgent(seed) if kind == "random" else (
        LanguageAgent(adapter=adapter, history_size=history_size) if kind == "model" else None)
    for game in selected:
        if game["game_id"] in completed_ids:
            continue
        if kind == "random":
            # Une RNG par jeu garantit la même trajectoire après interruption.
            game_seed = int(hashlib.sha256(f"{seed}:{game['game_id']}".encode()).hexdigest()[:16], 16)
            agent = RandomAgent(game_seed)
        episode, trace = rollout(game, agent, kind, max_steps)
        episodes.append(episode)
        write_jsonl(Path(output) / "traces" / f"{game['game_id']}.jsonl", trace)
        # Sauvegarder à chaque épisode pour conserver les résultats si interruption.
        write_jsonl(Path(output) / "episodes.jsonl", episodes)
    save_json(summary_path, dict(config=config, complete=True, metrics=summarize(episodes)))
    return summarize(episodes)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", default="artifacts/manifest.jsonl")
    p.add_argument("--output", default="artifacts/eval/base_easy")
    p.add_argument("--level", choices=["easy", "advanced"], default="easy")
    p.add_argument("--split", choices=["validation", "test"], default="test")
    p.add_argument("--kind", choices=["model", "random", "oracle"], default="model")
    p.add_argument("--adapter")
    p.add_argument("--history-size", type=int, default=4)
    p.add_argument("--max-steps", type=int, default=30)
    p.add_argument("--seed", type=int, default=42)
    print(evaluate(**vars(p.parse_args())))
