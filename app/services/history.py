import json
import os
from datetime import datetime


HISTORY_FILE = "app/data/history.json"


def load_history() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # PL: Pusty lub uszkodzony JSON traktujemy jak brak historii.
            # EN: Empty or corrupted JSON is treated as no history.
            return []


def save_analysis(password: str, analysis: dict) -> None:
    history = load_history()

    # PL: Nie zapisujemy samego hasla, tylko dane potrzebne do historii wynikow.
    # EN: The raw password is not saved, only data needed for result history.
    record = {
        "timestamp": datetime.now().isoformat(),
        "password_length": len(password),
        "score": analysis["score"],
        "strength": analysis["strength"],
        "entropy": analysis["entropy"]
    }

    history.append(record)

    # PL: indent=4 ulatwia podejrzenie historii podczas prezentacji lub debugowania.
    # EN: indent=4 keeps the history readable during demos and debugging.
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def get_history() -> list:
    return load_history()
