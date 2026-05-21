import json
import os
from datetime import datetime

DEFAULT_HISTORY_FILE = "app/data/history.json"
HISTORY_FILE_ENV = "PASSWORD_HISTORY_FILE"
MAX_HISTORY_RECORDS = 20


def get_history_file() -> str:
    return os.getenv(HISTORY_FILE_ENV, DEFAULT_HISTORY_FILE)


def load_history() -> list:
    history_file = get_history_file()

    if not os.path.exists(history_file):
        return []

    with open(history_file, encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # Treat an empty or corrupted history file as no history.
            return []


def save_analysis(password: str, analysis: dict) -> None:
    history = load_history()
    history_file = get_history_file()

    # Save only the metadata needed to show past results.
    record = {
        "timestamp": datetime.now().isoformat(),
        "password_length": len(password),
        "score": analysis["score"],
        "strength": analysis["strength"],
        "entropy": analysis["entropy"]
    }

    history.append(record)
    history = history[-MAX_HISTORY_RECORDS:]

    history_directory = os.path.dirname(history_file)
    if history_directory:
        os.makedirs(history_directory, exist_ok=True)

    # Keep the file readable for demos and quick debugging.
    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def get_history() -> list:
    return load_history()
