"""Rollouts, métriques au niveau des jeux et traces d'échec auditables."""
import argparse
import math
import statistics
import time
from pathlib import Path
from .common import read_jsonl, write_jsonl, save_json, public_observation
from .games import start_game, validate_manifest
from .agents import RandomAgent, LanguageAgent


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
            is_invalid = action not in admissible and action not in {"look", "inventory"}
            invalid += int(is_invalid)
            signature = (obs["description"], obs["inventory"], obs["feedback"], action)
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
    agent = RandomAgent(seed) if kind == "random" else (
        LanguageAgent(adapter=adapter, history_size=history_size) if kind == "model" else None)
    episodes = []
    for game in selected:
        episode, trace = rollout(game, agent, kind, max_steps)
        episodes.append(episode)
        write_jsonl(Path(output) / "traces" / f"{game['game_id']}.jsonl", trace)
        # Sauvegarder à chaque épisode pour conserver les résultats si interruption.
        write_jsonl(Path(output) / "episodes.jsonl", episodes)
    save_json(Path(output) / "summary.json", dict(config=dict(level=level, split=split,
        kind=kind, adapter=adapter, history_size=history_size, max_steps=max_steps, seed=seed),
        metrics=summarize(episodes)))
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
