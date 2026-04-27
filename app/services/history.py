import json
import os
from datetime import datetime


HISTORY_FILE = "app/data/history.json"


def load_history() -> list:
    """PL: Wczytuje historię analiz z pliku JSON. EN: Loads analysis history from a JSON file."""

    # PL: Brak pliku traktujemy jako pustą historię, co ułatwia pierwsze uruchomienie aplikacji.
    # EN: A missing file is treated as empty history, which simplifies first application startup.
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # PL: Uszkodzony lub pusty JSON nie powinien zatrzymywać działania API.
            # EN: Corrupted or empty JSON should not stop the API from working.
            return []


def save_analysis(password: str, analysis: dict) -> None:
    """PL: Zapisuje metadane analizy bez zapisywania jawnego hasła.
    EN: Saves analysis metadata without storing the raw password.
    """
    history = load_history()

    # PL: Dla bezpieczeństwa historia przechowuje długość hasła, wynik, siłę i entropię, ale nie hasło.
    # EN: For safety, history stores password length, score, strength, and entropy, but not the password.
    record = {
        "timestamp": datetime.now().isoformat(),
        "password_length": len(password),
        "score": analysis["score"],
        "strength": analysis["strength"],
        "entropy": analysis["entropy"]
    }

    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def get_history() -> list:
    """PL: Udostępnia historię analiz innym warstwom aplikacji. EN: Exposes analysis history to other layers."""
    return load_history()
