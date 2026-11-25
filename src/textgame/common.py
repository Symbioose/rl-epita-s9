"""Petits outils indépendants des bibliothèques de deep learning."""
import hashlib
import json
from pathlib import Path


def read_jsonl(path):
    with open(path, encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    temporary.replace(path)


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


SYSTEM = ("You play a text adventure. Achieve the objective. "
          "Reply with exactly one game command, without explanation or formatting.")


def public_observation(state):
    # Liste blanche : ni policy_commands, ni facts, ni walkthrough dans le prompt.
    return {key: str(state.get(key) or "")
            for key in ("feedback", "description", "inventory", "objective")}


def messages(history, observation, history_size=4):
    if history_size < 0:
        raise ValueError("history_size doit être positif ou nul")
    result = [{"role": "system", "content": SYSTEM}]
    for past in (history[-history_size:] if history_size else []):
        result += [{"role": "user", "content": format_observation(past["observation"])},
                   {"role": "assistant", "content": past["action"]}]
    result.append({"role": "user", "content": format_observation(observation)})
    return result


def format_observation(observation):
    return "\n".join(f"{key.upper()}: {observation.get(key, '')}" for key in
                     ("objective", "description", "inventory", "feedback"))


def normalize_action(text):
    lines = text.strip().splitlines()
    return lines[0].strip().strip('`').strip() if lines else ""
