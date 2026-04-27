from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """PL: Endpoint główny powinien potwierdzać działanie API. EN: Root endpoint should confirm API availability."""
    response = client.get("/api/")

    assert response.status_code == 200
    assert response.json()[
        "message"] == "Password Security Analyzer API is running"


def test_analyze_endpoint():
    """PL: Analiza hasła powinna zwrócić kluczowe metryki bezpieczeństwa. EN: Password analysis should return key metrics."""
    response = client.post(
        "/api/analyze",
        json={"password": "StrongPassword123!"}
    )

    assert response.status_code == 200
    assert "score" in response.json()
    assert "strength" in response.json()
    assert "entropy" in response.json()


def test_generate_endpoint():
    """PL: Generator powinien respektować żądaną długość hasła. EN: Generator should respect requested password length."""
    response = client.get("/api/generate?length=20")

    assert response.status_code == 200
    assert len(response.json()["password"]) == 20


def test_compare_endpoint():
    """PL: Porównanie powinno wskazać hasło z wyższym wynikiem. EN: Comparison should identify the higher-scored password."""
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
    """PL: Endpoint porad powinien zwrócić listę zaleceń. EN: Tips endpoint should return a list of recommendations."""
    response = client.get("/api/tips")

    assert response.status_code == 200
    assert "tips" in response.json()
