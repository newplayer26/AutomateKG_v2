
from .llm.openai import OpenAIChat
from .llm.huggingface import HuggingFaceChat
from .llm.basellm import BaseLLM

def get_llm(choice, model_name, token, notify_callback) -> BaseLLM:
    
    if (choice == "OPENAI"):
        model = OpenAIChat(openai_api_key=token,
                           model_name=model_name,
                           notify_callback=notify_callback)
        return model
    elif (choice == "HUGGINGFACE"):
        model = HuggingFaceChat(model_name=model_name,
                                hf_token=token, notify_callback=notify_callback)
        return model
