import sys

import ollama


def summarize(model_name: str, prompt: str, text: str) -> str:
    try:
        # Find all cached model names
        models = ollama.list()["models"]
        cached = [model["name"] for model in models]
        # Download the specified model if it is not already cached
        if model_name not in cached:
            ollama.pull(model_name)
        response = ollama.generate(model_name, prompt + text)
        return response["response"]
    except Exception:
        print("Error: Ollama is not running. Run the server with `ollama serve`.")
        sys.exit(1)
