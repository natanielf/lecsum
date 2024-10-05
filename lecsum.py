#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import warnings
import yaml

# Default configuration
DEFAULT_WHISPER_MODEL = "base.en"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
DEFAULT_PROMPT = "Summarize: "

# Common paths that may contain a configuration file
CONFIG_FILE = "lecsum.yaml"
CONFIG_FILE_PATHS = [
    Path.cwd().joinpath(CONFIG_FILE),  # ./
    Path.home().joinpath(".config", CONFIG_FILE),  # ~/.config/
]


# Parse command-line arguments
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="lecsum",
        description="Automatically transcribe and summarize lecture recordings.",
    )
    parser.add_argument("file", help="name of an audio file")
    parser.add_argument("-c", "--config", help="'lecsum.yaml' configuration file")

    return parser.parse_args()


# Parse YAML config file
def load_config(path: str = None) -> dict:
    # Default configuration
    default = {
        "whisper_model": DEFAULT_WHISPER_MODEL,
        "ollama_model": DEFAULT_OLLAMA_MODEL,
        "prompt": DEFAULT_PROMPT,
    }

    # Parse a yaml file, immediately exiting if any errors are found
    def load_yaml_file(path: str = None) -> dict:
        try:
            return yaml.load(open(path, "r").read(), Loader=yaml.Loader)
        except yaml.YAMLError as e:
            print(f"Error in configuration file '{path}': {e}")
            os.exit(1)

    # Default to path passed via command-line
    if path:
        p = Path(path)
        if p.exists() and p.is_file():
            return load_yaml_file(path)
        else:
            os.exit(1)

    # If a config file is not specified, check a couple default locations
    for p in CONFIG_FILE_PATHS:
        if p.exists() and p.is_file():
            return load_yaml_file(p)

    # Use the default configuration if a config file cannot be found
    return default


def main():
    # Parse command-line arguments
    args = parse_args()
    # Parse configuration file
    config = load_config(args.config)

    # Ignore module warnings
    warnings.simplefilter("ignore")
    # Only import modules if the configuration is valid
    from modules.transcribe import transcribe
    from modules.summarize import summarize

    # File name without suffix
    name = Path(args.file).stem

    # Transcribe the audio file
    transcript = transcribe(model_name=config["whisper_model"], audio_file=args.file)

    with open(Path.cwd().joinpath(f"{name}_transcript.txt"), "w") as f:
        f.write(transcript)

    # Summarize the transcription
    summary = summarize(
        model_name=config["ollama_model"], prompt=config["prompt"], text=transcript
    )

    # Write the summary to a text file
    with open(Path.cwd().joinpath(f"{name}_summary.txt"), "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
