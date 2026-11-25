"""Démo live : affiche la commande du SLM et la réponse du jeu."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textgame.agents import LanguageAgent
from textgame.common import public_observation
from textgame.games import start_game


def main(game, adapter, steps):
    agent = LanguageAgent(adapter=adapter)
    env, history = start_game(game), []
    try:
        state = env.reset()
        print(state.feedback)
        for _ in range(steps):
            obs = public_observation(state)
            action = agent.act(history, obs)
            print(f"\n> {action}")
            state, score, done = env.step(action)
            print(state.feedback)
            history.append(dict(observation=obs, action=action))
            if done:
                print(f"Fin : victoire={state.won}, score={score}")
                break
    finally:
        env.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("game")
    p.add_argument("--adapter")
    p.add_argument("--steps", type=int, default=30)
    main(**vars(p.parse_args()))
