from pathlib import Path

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

from lecsum import DEFAULT_CONFIG, transcribe_and_summarize
from modules.transcribe import transcribe
from modules.summarize import summarize
from modules.utils import check_config, write

app = FastAPI()


class Config(BaseModel):
    whisper_model: str = DEFAULT_CONFIG["whisper_model"]
    ollama_model: str = DEFAULT_CONFIG["ollama_model"]
    prompt: str = DEFAULT_CONFIG["prompt"]
    file: str = None


@app.post("/summarize", status_code=status.HTTP_200_OK)
async def create_summary(config: Config, response: Response):
    print("DEBUG: create summary", config)
    check_config(whisper_model=config.whisper_model, ollama_model=config.ollama_model)
    path = Path(config.file)
    if not path.is_file():
        print(f"Error: Audio file '{path}' cannot be opened.")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Error: Audio file '{path}' cannot be opened."}
    transcript, summary = transcribe_and_summarize(
        whisper_model=config.whisper_model,
        ollama_model=config.ollama_model,
        prompt=config.prompt,
        file=config.file,
    )
    # transcript = transcribe(model_name=config.whisper_model, audio_file=config.filename)
    # summary = summarize(
    #     model_name=config.ollama_model, prompt=config.prompt, text=transcript
    # )
    return {"message": summary}
