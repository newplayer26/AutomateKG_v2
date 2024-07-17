from typing import (
    Callable,
    List,
)

import openai
import tiktoken
from .basellm import BaseLLM
from retry import retry

OpenAI = openai.OpenAI


class OpenAIChat(BaseLLM):
    """Wrapper around OpenAI Chat large language models."""

    def __init__(
        self,
        openai_api_key: str,
        model_name: str = "gpt-3.5-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.0,
        notify_callback=None
    ) -> None:
        self.notify = notify_callback
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model_name
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
            completions = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=messages,
            )
            return completions.choices[0].message.content

        except openai.error.InvalidRequestError as e:
            return str(f"Error: {e}")
        except openai.error.AuthenticationError as e:
            return "Error: The provided OpenAI API key is invalid"
        except Exception as e:
            print(f"Retrying LLM call {e}")
            raise Exception()

    def num_tokens_from_string(self, string: str) -> int:
        encoding = tiktoken.encoding_for_model(self.model)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def max_allowed_token_length(self) -> int:
        return 2049
