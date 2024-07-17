import sys
from llm_cache import set_cached_llm





def main():
    choice = sys.argv[1]
    model_name = sys.argv[2]
    token = None if sys.argv[3] == 'None' else sys.argv[3]
    try:
        set_cached_llm(choice, model_name, token)
        print(f"LLM set to {choice} with model {model_name}")
    except ValueError as e:
        print(f"Error setting LLM: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
