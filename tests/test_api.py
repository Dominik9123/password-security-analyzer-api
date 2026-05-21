import string

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def use_temp_history_file(history_file_path):
    return history_file_path


def test_root_endpoint():
    """The root endpoint should confirm that the API is available."""
    response = client.get("/api/")

    assert response.status_code == 200
    assert response.json()[
        "message"] == "Password Security Analyzer API is running"


def test_analyze_endpoint():
    """Password analysis should return the main security metrics."""
    response = client.post(
        "/api/analyze",
        json={"password": "StrongPassword123!"}
    )

    assert response.status_code == 200
    assert "score" in response.json()
    assert "strength" in response.json()
    assert "entropy" in response.json()


def test_generate_endpoint():
    """The generator should respect the requested password length."""
    response = client.get("/api/generate?length=20")

    assert response.status_code == 200
    assert len(response.json()["password"]) == 20


def test_compare_endpoint():
    """Password comparison should identify the higher-scored password."""
    response = client.post(
        "/api/compare",
        json={
            "first_password": "test123",
            "second_password": "StrongPassword123!"
        }
    )

    assert response.status_code == 200
    assert response.json()["stronger_password"] == "second_password"


def test_tips_endpoint():
    """The tips endpoint should return a list of recommendations."""
    response = client.get("/api/tips")

    assert response.status_code == 200
    assert "tips" in response.json()


def test_generate_endpoint_supports_options():
    response = client.get(
        "/api/generate?length=20&include_numbers=false"
        "&include_symbols=false&avoid_ambiguous=true"
    )

    password = response.json()["password"]

    assert response.status_code == 200
    assert len(password) == 20
    assert not any(char.isdigit() for char in password)
    assert not any(char in string.punctuation for char in password)
    assert not any(char in "O0Il1" for char in password)
