import whisper


def transcribe(model_name: str, audio_file: str) -> str:
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_file)
    return result["text"]
