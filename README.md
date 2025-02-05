# lecsum

Automatically transcribe and summarize lecture recordings completely on-device using AI.

## Environment Setup

Install [Ollama](https://ollama.com/download).

Create a virtual Python environment:

```sh
python3 -m venv .venv
```

Activate the virtual environment:

```sh
source .venv/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

## Configuration (optional)

Edit `lecsum.yaml`:

| **Field**       | **Default Value** | **Possible Values**                                                                    | **Description**                                                  |
| --------------- | ----------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `whisper_model` | "base.en"         | [Whisper model name](https://github.com/openai/whisper#available-models-and-languages) | Specifies which Whisper model to use for transcription           |
| `ollama_model`  | "llama3.1:8b"     | [Ollama model name](https://ollama.com/library)                                        | Specifies which Ollama model to use for summarization            |
| `prompt`        | "Summarize: "     | Any string                                                                             | Instructs the large language model during the summarization step |

## Usage

Run the Ollama server:

```sh
ollama serve
```

### Command-line

In a new terminal, run:

```sh
./lecsum.py -c [CONFIG_FILE] [AUDIO_FILE]
```

Use any file format supported by [Whisper](https://platform.openai.com/docs/guides/speech-to-text) (`mp3`, `mp4`, `wav`, `webm`, etc.).

### Server

To start the `lecsum` server in a development environment, run:

```sh
fastapi dev server.py
```

### Testing

Automated testing is performed using the `pytest` framework:

```sh
pytest
```

## References

- https://pyyaml.org/wiki/PyYAMLDocumentation
- https://github.com/openai/whisper
- https://github.com/ollama/ollama-python
- https://fastapi.tiangolo.com
