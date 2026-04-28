# Password Security Analyzer API

Prosty projekt w FastAPI do sprawdzania siły hasła. Aplikacja potrafi ocenić hasło w skali 0-100, policzyć przybliżoną entropię, wskazać problemy, wygenerować losowe hasło i porównać dwa hasła ze sobą.

Hasła nie są zapisywane w historii. Backend przechowuje tylko metadane analizy, takie jak długość hasła, wynik, poziom siły i entropia.

## Funkcje

- analiza hasła i klasyfikacja `weak`, `medium`, `strong`,
- sprawdzanie długości, cyfr, małych i wielkich liter oraz znaków specjalnych,
- wykrywanie prostych wzorców z pliku `weak_passwords.txt`,
- wykrywanie powtarzających się znaków, np. `aaa` albo `111`,
- generowanie haseł o wybranej długości,
- porównywanie dwóch haseł,
- historia analiz bez zapisywania jawnych haseł,
- prosty frontend w katalogu `frontend`.

## Technologie

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTML, CSS, JavaScript

## Uruchomienie

Utwórz i aktywuj środowisko:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

Uruchom API:

```bash
uvicorn app.main:app --reload
```

API będzie dostępne tutaj:

```text
http://127.0.0.1:8000/api/
```

Dokumentacja Swagger:

```text
http://127.0.0.1:8000/docs
```

Frontend można odpalić przez `frontend/index.html`, np. z Live Servera w VS Code.

Uwaga: analiza hasła aktualizuje `app/data/history.json`. Jeżeli używasz Live Servera, plik `.vscode/settings.json` ignoruje ten zapis, żeby strona nie odświeżała się po każdej analizie.

## Endpointy

| Metoda | Endpoint                  | Opis |
| ------ | ------------------------- | ---- |
| GET    | `/api/`                   | Sprawdzenie, czy API działa |
| POST   | `/api/analyze`            | Analiza jednego hasła |
| GET    | `/api/generate?length=16` | Wygenerowanie hasła |
| GET    | `/api/tips`               | Proste porady dotyczące haseł |
| GET    | `/api/history`            | Historia analiz |
| POST   | `/api/compare`            | Porównanie dwóch haseł |

## Przykład

```http
POST /api/analyze
Content-Type: application/json
```

```json
{
  "password": "StrongPassword123!"
}
```

Przykładowa odpowiedź:

```json
{
  "score": 90,
  "strength": "strong",
  "entropy": 104.92,
  "issues": [],
  "suggestions": []
}
```

## Struktura

```text
app/
  api/
    routes.py
  data/
    history.json
    weak_passwords.txt
  models/
    schemas.py
  services/
    analyzer.py
    generator.py
    history.py
  main.py
frontend/
  index.html
  script.js
  style.css
tests/
  test_analyzer.py
  test_api.py
  test_generator.py
```

## Testy

```bash
pytest
```

Testy sprawdzają logikę analizatora, generator haseł i główne endpointy API.

## Pomysły na rozbudowę

- baza danych zamiast pliku JSON,
- limit zapytań do API,
- dłuższa lista słabych haseł,
- integracja z bazą wycieków haseł,
- dokładniejszy algorytm oceny.

## English

Password Security Analyzer API is a small FastAPI project for checking password strength. It scores a password from 0 to 100, estimates entropy, returns issues and suggestions, generates random passwords and compares two passwords.

Raw passwords are not stored in history. The backend saves only analysis metadata, such as password length, score, strength level and entropy.

## Features

- password analysis with `weak`, `medium` and `strong` classification,
- checks for length, digits, lowercase letters, uppercase letters and special characters,
- detection of simple weak patterns from `weak_passwords.txt`,
- detection of repeated characters, for example `aaa` or `111`,
- password generation with selected length,
- comparison of two passwords,
- analysis history without storing raw passwords,
- simple frontend in the `frontend` directory.

## Technologies

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTML, CSS, JavaScript

## Running The Project

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000/api/
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

The frontend can be opened from `frontend/index.html`, for example with VS Code Live Server.

Note: password analysis updates `app/data/history.json`. If you use Live Server, `.vscode/settings.json` ignores this file so the page does not refresh after every analysis.

## API Endpoints

| Method | Endpoint                  | Description |
| ------ | ------------------------- | ----------- |
| GET    | `/api/`                   | Checks whether the API is running |
| POST   | `/api/analyze`            | Analyzes one password |
| GET    | `/api/generate?length=16` | Generates a password |
| GET    | `/api/tips`               | Returns simple password tips |
| GET    | `/api/history`            | Returns analysis history |
| POST   | `/api/compare`            | Compares two passwords |

## Example

```http
POST /api/analyze
Content-Type: application/json
```

```json
{
  "password": "StrongPassword123!"
}
```

Example response:

```json
{
  "score": 90,
  "strength": "strong",
  "entropy": 104.92,
  "issues": [],
  "suggestions": []
}
```

## Tests

```bash
pytest
```

The tests cover the analyzer logic, password generator and main API endpoints.
