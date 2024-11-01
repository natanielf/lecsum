import sys

import httpx
import ollama


def summarize(model_name: str, prompt: str, text: str) -> str:
    try:
        response = ollama.generate(model_name, prompt + text)
        return response["response"]
    except httpx.ConnectError:
        print("Error: Ollama is not running. Run the server with `ollama serve`.")
        sys.exit(1)
