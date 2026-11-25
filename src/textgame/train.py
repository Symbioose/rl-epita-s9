"""Fine-tuning supervisé LoRA. Aucun calcul de politique RL dans cette étape."""
import argparse
import importlib.metadata
import time
from pathlib import Path
from .common import read_jsonl, save_json, digest
from .tokenization import encode_example, pad_examples

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"


def train(train_path, validation_path, output, model=MODEL, history_size=4,
          epochs=3, max_steps=-1, seed=42, max_length=1024):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, set_seed
    from peft import LoraConfig, get_peft_model, TaskType
    set_seed(seed)
    train_rows, validation_rows = read_jsonl(train_path), read_jsonl(validation_path)
    if not train_rows or not validation_rows:
        raise ValueError("Entraînement et validation doivent être non vides")
    if {r["game_id"] for r in train_rows} & {r["game_id"] for r in validation_rows}:
        raise ValueError("Fuite : jeux partagés entre train et validation")
    tokenizer = AutoTokenizer.from_pretrained(model)
    tokenizer.pad_token = tokenizer.eos_token
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    base = AutoModelForCausalLM.from_pretrained(model, torch_dtype=dtype,
                                               attn_implementation="eager")
    base.config.use_cache = False
    adapted = get_peft_model(base, LoraConfig(task_type=TaskType.CAUSAL_LM,
        r=16, lora_alpha=32, lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"]))
    adapted.print_trainable_parameters()
    train_data = [encode_example(tokenizer, r, history_size, max_length) for r in train_rows]
    val_data = [encode_example(tokenizer, r, history_size, max_length) for r in validation_rows]

    def collate(examples):
        return {k: torch.tensor(v, dtype=torch.long)
                for k, v in pad_examples(examples, tokenizer.pad_token_id).items()}

    arguments = TrainingArguments(output_dir=str(Path(output) / "checkpoints"),
        num_train_epochs=epochs, max_steps=max_steps, per_device_train_batch_size=2,
        per_device_eval_batch_size=2, gradient_accumulation_steps=8,
        learning_rate=2e-4, warmup_ratio=0.1, weight_decay=0.01,
        eval_strategy="epoch", save_strategy="epoch", load_best_model_at_end=True,
        metric_for_best_model="eval_loss", greater_is_better=False, save_total_limit=1,
        fp16=torch.cuda.is_available(), logging_steps=5, report_to="none", seed=seed,
        dataloader_num_workers=0, use_mps_device=False)
    runner = Trainer(model=adapted, args=arguments, train_dataset=train_data,
                     eval_dataset=val_data, data_collator=collate)
    begin = time.monotonic()
    result = runner.train()
    runner.save_model(output)
    tokenizer.save_pretrained(output)
    save_json(Path(output) / "training.json", dict(model=model, seed=seed,
        history_size=history_size, max_length=max_length, epochs=epochs,
        max_steps=max_steps, train_examples=len(train_rows), validation_examples=len(validation_rows),
        train_sha256=digest(train_path), validation_sha256=digest(validation_path),
        elapsed_seconds=time.monotonic()-begin, metrics=result.metrics,
        trainable_parameters=sum(p.numel() for p in adapted.parameters() if p.requires_grad),
        total_parameters=sum(p.numel() for p in adapted.parameters()),
        base_commit=getattr(base.config, "_commit_hash", None),
        versions={p: importlib.metadata.version(p) for p in ["torch", "transformers", "peft", "textworld"]},
        logs=runner.state.log_history))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--train-path", default="artifacts/data/easy_train.jsonl")
    p.add_argument("--validation-path", default="artifacts/data/easy_validation.jsonl")
    p.add_argument("--output", default="artifacts/lora_easy")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--history-size", type=int, default=4)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--max-steps", type=int, default=-1)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-length", type=int, default=1024)
    train(**vars(p.parse_args()))
