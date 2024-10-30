# lecsum

Automatically transcribe and summarize lecture recordings completely on-device using AI.

## Environment Setup

Install [Ollama](https://ollama.com/download).

Create a virtual Python environment:

```sh
python3 -m venv venv
```

Activate the virtual environment:

```sh
source venv/bin/activate
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

## Run

Run the Ollama server:

```sh
ollama serve
```

In a new terminal, run:

```sh
./lecsum.py -c [CONFIG_FILE] [AUDIO_FILE]
```

## References

- https://pyyaml.org/wiki/PyYAMLDocumentation
- https://github.com/openai/whisper
- https://github.com/ollama/ollama-python
