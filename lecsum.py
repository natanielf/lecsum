#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import warnings

import yaml

from modules.transcribe import transcribe
from modules.summarize import summarize
from modules.utils import check_config, write

# Default configuration
DEFAULT_CONFIG = {
    "whisper_model": "base.en",
    "ollama_model": "llama3.1:8b",
    "prompt": "Summarize: ",
}

# Common paths that may contain a configuration file
CONFIG_FILE = "lecsum.yaml"
CONFIG_FILE_PATHS = [
    Path.cwd().joinpath(CONFIG_FILE),  # ./
    Path.home().joinpath(".config", CONFIG_FILE),  # ~/.config/
]


# Parse command-line arguments
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatically transcribe and summarize lecture recordings.",
    )
    parser.add_argument("file", help="name of an audio file", type=str)
    parser.add_argument(
        "-c",
        "--config",
        help=f"'{CONFIG_FILE}' configuration file",
        type=str,
    )
    return parser.parse_args()


# Parse YAML config file
def load_config(path: str) -> dict | None:
    # Parse a yaml file
    def load_yaml_file(path: Path) -> dict | None:
        try:
            return yaml.load(open(path, "r").read(), Loader=yaml.Loader)
        except yaml.YAMLError as e:
            print(f"Error in configuration file '{path}': {e}")
            return

    # Default to path passed via command-line
    if path:
        p = Path(path)
        if p.is_file():
            return load_yaml_file(p)
        else:
            print(f"Error: Configuration file '{p}' cannot be opened.")
            return

    # If a config file is not specified, check a couple default locations
    for p in CONFIG_FILE_PATHS:
        if p.is_file():
            return load_yaml_file(p)

    # Use the default configuration if a config file cannot be found
    return DEFAULT_CONFIG


def transcribe_and_summarize(
    whisper_model: str, ollama_model: str, prompt: str, file: str
) -> tuple[str, str]:
    path = Path(file)
    filename = path.stem
    parent = path.resolve().parent
    # Transcribe the audio file
    transcript = transcribe(model_name=whisper_model, audio_file=file)

    # Write the transcript to a text file
    write(path=parent.joinpath(f"{filename}_transcript.txt"), text=transcript)

    # Summarize the transcription
    summary = summarize(model_name=ollama_model, prompt=prompt, text=transcript)

    # Write the summary to a text file
    write(path=parent.joinpath(f"{filename}_summary.txt"), text=summary)

    return (transcript, summary)


def main():
    # Ignore module warnings
    warnings.simplefilter("ignore")

    # Parse command-line arguments
    args = parse_args()
    # Parse configuration file
    config = load_config(args.config)
    # Exit if an error is found in the config file
    if not config:
        sys.exit(1)
    # Path to audio file
    path = Path(args.file)
    if not path.is_file():
        print(f"Error: Audio file '{path}' cannot be opened.")
        sys.exit(1)

    # Ensure the configuration is valid
    check_config(
        whisper_model=config["whisper_model"], ollama_model=config["ollama_model"]
    )

    # Transcribe and summarize the audio file
    transcribe_and_summarize(
        whisper_model=config["whisper_model"],
        ollama_model=config["ollama_model"],
        prompt=config["prompt"],
        file=args.file,
    )


if __name__ == "__main__":
    main()
