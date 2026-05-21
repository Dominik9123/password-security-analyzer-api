import json

from app.services.history import load_history, save_analysis


def test_load_history_returns_empty_when_file_is_missing(history_file_path):
    assert load_history() == []


def test_load_history_returns_empty_list_for_corrupted_json(history_file_path):
    history_file_path.write_text("{broken json", encoding="utf-8")

    assert load_history() == []


def test_save_analysis_does_not_store_raw_password(history_file_path):
    analysis = {
        "score": 90,
        "strength": "strong",
        "entropy": 104.92
    }

    save_analysis("SecretPassword123!", analysis)

    saved_history = json.loads(history_file_path.read_text(encoding="utf-8"))

    assert len(saved_history) == 1
    assert saved_history[0]["password_length"] == len("SecretPassword123!")
    assert saved_history[0]["score"] == 90
    assert saved_history[0]["strength"] == "strong"
    assert saved_history[0]["entropy"] == 104.92
    assert "SecretPassword123!" not in history_file_path.read_text(encoding="utf-8")


def test_save_analysis_keeps_only_latest_history_records(history_file_path):
    analysis = {
        "score": 50,
        "strength": "medium",
        "entropy": 45.0
    }

    for index in range(25):
        save_analysis(f"Password{index}!", analysis)

    saved_history = json.loads(history_file_path.read_text(encoding="utf-8"))

    assert len(saved_history) == 20
    assert saved_history[0]["password_length"] == len("Password5!")
    assert saved_history[-1]["password_length"] == len("Password24!")
