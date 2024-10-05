import ollama


def summarize(model_name: str, prompt: str, text: str) -> str:
    # Find all cached model names
    cached = [model["name"] for model in ollama.list()["models"]]
    # Download the specified model if it is not already cached
    if model_name not in cached:
        ollama.pull(model_name)
    response = ollama.generate(model_name, prompt + text)
    return response["response"]
