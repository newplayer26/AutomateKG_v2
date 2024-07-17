from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List
from retry import retry
from .basellm import BaseLLM
from huggingface_hub import login


class HuggingFaceChat(BaseLLM):
    """Wrapper around Hugging Face Transformers large language models."""

    def __init__(
        self,
        model_name: str = "gpt2",
        max_tokens: int = 1000,
        hf_token: str = None,
        temperature: float = 0.0,
        notify_callback=None
    ) -> None:
        self.notify = notify_callback
        self.notify("init", f"Initializing HuggingFace model {model_name}")
        if (hf_token):
            login(token=hf_token)
            self.notify("auth", "Authenticated with HuggingFace")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.max_tokens = max_tokens
        self.temperature = temperature

    @retry(tries=3, delay=1)
    def notify(self, event: str, message: str):
        if self.notify_callback:
            self.notify_callback(event, message)
        else:
            print(f"{event}: {message}")

    def generate(
        self,
        messages: List[str],
    ) -> str:
        try:
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(self.model.device)
            terminators = [
                self.tokenizer.eos_token_id,
                self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_length=input_ids.shape[1] + self.max_tokens,
                    temperature=self.temperature,
                    eos_token_id=terminators,
                    do_sample=True if self.temperature > 0 else False,
                )
            response = outputs[0][input_ids.shape[-1]:]
            generated_text = self.tokenizer.decode(
                response, skip_special_tokens=True)
            torch.cuda.empty_cache()
            return generated_text
        except Exception as e:
            print(f"Retrying LLM call {e}")

    def num_tokens_from_string(self, string: str) -> int:
        return len(self.tokenizer.encode(string))

    def max_allowed_token_length(self) -> int:
        return self.model.config.max_position_embeddings
