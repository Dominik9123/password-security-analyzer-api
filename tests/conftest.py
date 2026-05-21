import re
from pathlib import Path

import pytest


@pytest.fixture
def history_file_path(monkeypatch, request):
    safe_name = re.sub(r"[^a-zA-Z0-9_]+", "_", request.node.nodeid)
    history_dir = Path("test-artifacts") / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    history_file = history_dir / f"{safe_name}.json"
    if history_file.exists():
        history_file.unlink()

    monkeypatch.setenv("PASSWORD_HISTORY_FILE", str(history_file))

    yield history_file

    if history_file.exists():
        history_file.unlink()
