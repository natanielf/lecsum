#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import warnings
import yaml

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
def load_config(path: str = None) -> dict:
    # Parse a yaml file, immediately exiting if any errors are found
    def load_yaml_file(path: Path = None) -> dict:
        try:
            return yaml.load(open(path, "r").read(), Loader=yaml.Loader)
        except yaml.YAMLError as e:
            print(f"Error in configuration file '{path}': {e}")
            sys.exit(1)

    # Default to path passed via command-line
    if path:
        p = Path(path)
        if p.exists() and p.is_file():
            return load_yaml_file(p)
        else:
            print(f"Error: Configuration file '{p}' cannot be opened.")
            sys.exit(1)

    # If a config file is not specified, check a couple default locations
    for p in CONFIG_FILE_PATHS:
        if p.exists() and p.is_file():
            return load_yaml_file(p)

    # Use the default configuration if a config file cannot be found
    return DEFAULT_CONFIG


def main():
    # Ignore module warnings
    warnings.simplefilter("ignore")

    # Parse command-line arguments
    args = parse_args()
    # Parse configuration file
    config = load_config(args.config)
    # Path to audio file
    path = Path(args.file)
    if not (path.exists() and path.is_file()):
        print(f"Error: Audio file '{path}' cannot be opened.")
        sys.exit(1)

    file = path.stem
    parent = path.resolve().parent

    # Only import modules if the configuration is valid
    from modules.transcribe import transcribe
    from modules.summarize import summarize
    from modules.utils import check_whisper_config, check_ollama_config

    # Ensure the configuration is valid
    check_whisper_config(config["whisper_model"])
    check_ollama_config(config["ollama_model"])

    # Transcribe the audio file
    transcript = transcribe(model_name=config["whisper_model"], audio_file=args.file)

    # Write the transcript to a text file
    with open(parent.joinpath(f"{file}_transcript.txt"), "w") as f:
        f.write(transcript)

    # Summarize the transcription
    summary = summarize(
        model_name=config["ollama_model"], prompt=config["prompt"], text=transcript
    )

    # Write the summary to a text file
    with open(parent.joinpath(f"{file}_summary.txt"), "w") as f:
        f.write(summary)


if __name__ == "__main__":
    main()
