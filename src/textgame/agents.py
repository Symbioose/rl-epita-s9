"""L'agent génératif reçoit uniquement une observation publique et son historique."""
import random
from .common import messages, normalize_action


class RandomAgent:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)

    def act(self, history, observation, admissible):
        return self.rng.choice(sorted(admissible)) if admissible else "look"


class LanguageAgent:
    def __init__(self, model="Qwen/Qwen2.5-0.5B-Instruct", adapter=None, history_size=4):
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        self.torch = torch
        self.history_size = history_size
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForCausalLM.from_pretrained(model,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            attn_implementation="eager")
        if adapter:
            from peft import PeftModel
            self.model = PeftModel.from_pretrained(self.model, adapter)
        self.model.to("cuda" if torch.cuda.is_available() else "cpu").eval()

    def act(self, history, observation):
        prompt = messages(history, observation, self.history_size)
        while True:
            inputs = self.tokenizer.apply_chat_template(prompt, tokenize=True,
                add_generation_prompt=True, return_tensors="pt", return_dict=True)
            if inputs["input_ids"].shape[-1] <= 1024:
                break
            if len(prompt) <= 2:
                raise ValueError("Observation trop longue pour le budget de contexte")
            del prompt[1:3]
        inputs = inputs.to(self.model.device)
        with self.torch.inference_mode():
            output = self.model.generate(**inputs, do_sample=False, max_new_tokens=32,
                pad_token_id=self.tokenizer.eos_token_id)
        return normalize_action(self.tokenizer.decode(
            output[0, inputs["input_ids"].shape[-1]:], skip_special_tokens=True))
