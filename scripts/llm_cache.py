
from python_lib.notify_callback import notify_callback
from python_lib.get_llm import get_llm
import json
import os
import sys
# print the current working directory


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LLM_CACHE_FILE = os.path.join(SCRIPT_DIR, 'llm_cache.json')
_llm_instance = None


def get_cached_llm():
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    if os.path.exists(LLM_CACHE_FILE):
        with open(LLM_CACHE_FILE, 'r') as f:
            config = json.load(f)

        _llm_instance = get_llm(
            config['choice'],
            config['model_name'],
            config.get('token'),
            notify_callback
        )
        return _llm_instance
    else:
        raise ValueError("LLM not configured. Please set up the LLM first.")


def set_cached_llm(choice, model_name, token=None):
    global _llm_instance
    _llm_instance = get_llm(choice, model_name, token, notify_callback)

    config = {
        "choice": choice,
        "model_name": model_name,
        "token": token
    }
    with open(LLM_CACHE_FILE, 'w') as f:
        json.dump(config, f)


def clear_cached_llm():
    global _llm_instance
    _llm_instance = None
    if os.path.exists(LLM_CACHE_FILE):
        os.remove(LLM_CACHE_FILE)
