"""Masquage de la loss : seuls les tokens de l'action servent de cibles."""
from .common import messages


def encode_example(tokenizer, example, history_size=4, max_length=1024):
    prompt_messages = messages(example["history"], example["observation"], history_size)
    # Retirer les tours les plus anciens avant de tronquer un contexte.
    while True:
        prefix = tokenizer.apply_chat_template(prompt_messages, tokenize=True,
                                               add_generation_prompt=True)
        full = tokenizer.apply_chat_template(
            prompt_messages + [{"role": "assistant", "content": example["action"]}],
            tokenize=True, add_generation_prompt=False)
        if full[:len(prefix)] != prefix:
            raise ValueError("Le template du tokenizer ne conserve pas le préfixe")
        if len(full) <= max_length:
            break
        if len(prompt_messages) > 2:
            del prompt_messages[1:3]
        else:
            # Ne jamais perdre silencieusement l'objectif ou la cible.
            raise ValueError("Observation trop longue : augmenter max_length")
    labels = [-100] * len(prefix) + full[len(prefix):]
    if not any(label != -100 for label in labels):
        raise ValueError("Exemple sans token cible")
    return dict(input_ids=full, attention_mask=[1] * len(full), labels=labels)


def pad_examples(examples, pad_token_id):
    length = max(len(e["input_ids"]) for e in examples)
    batch = {key: [] for key in ("input_ids", "attention_mask", "labels")}
    for e in examples:
        padding = length - len(e["input_ids"])
        for key, fill in (("input_ids", pad_token_id), ("attention_mask", 0), ("labels", -100)):
            batch[key].append(e[key] + [fill] * padding)
    return batch
