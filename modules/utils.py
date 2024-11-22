import sys
from pathlib import Path

import httpx
import ollama
import whisper


def check_whisper_config(whisper_model: str) -> None:
    if whisper_model not in whisper.available_models():
        print(f"Error: Whisper model '{whisper_model}' does not exist.")
        sys.exit(1)


def check_ollama_config(ollama_model: str) -> None:
    try:
        # Find all cached model names
        models = ollama.list()["models"]
        cached = [model["name"] for model in models]
        # Download the specified model if it is not already cached
        if ollama_model not in cached:
            ollama.pull(ollama_model)
    except ollama._types.ResponseError:
        print(f"Error: Ollama model '{ollama_model}' does not exist.")
        sys.exit(1)
    except httpx.ConnectError:
        print("Error: Ollama is not running. Run the server with `ollama serve`.")
        sys.exit(1)


def check_config(whisper_model: str, ollama_model: str) -> None:
    check_whisper_config(whisper_model)
    check_ollama_config(ollama_model)


def write(path: Path, text: str) -> None:
    with open(path, "w") as f:
        f.write(text)
