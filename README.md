# Password Security Analyzer API

[![Run Python Tests](https://github.com/Dominik9123/password-security-analyzer-api/actions/workflows/tests.yml/badge.svg)](https://github.com/Dominik9123/password-security-analyzer-api/actions/workflows/tests.yml)

Professional FastAPI-based password security analysis tool with password strength scoring, entropy calculation, secure password generation, comparison tools, history tracking, frontend UI, and automated testing.

# Password Security Analyzer API

Prosty projekt w FastAPI do sprawdzania siły hasła. Aplikacja potrafi ocenić hasło w skali 0-100, policzyć przybliżoną entropię, wskazać problemy, wygenerować losowe hasło i porównać dwa hasła ze sobą.

Hasła nie są zapisywane w historii. Backend przechowuje tylko metadane analizy, takie jak długość hasła, wynik, poziom siły i entropia.

> README zostało przygotowane i zaktualizowane z pomocą Codexa.

## Funkcje

- analiza hasła i klasyfikacja `weak`, `medium`, `strong`,
- sprawdzanie długości, cyfr, małych i wielkich liter oraz znaków specjalnych,
- wykrywanie prostych wzorców z pliku `weak_passwords.txt`,
- wykrywanie powtarzających się znaków, np. `aaa` albo `111`,
- wykrywanie sekwencji, np. `abcd`, `1234`, `9876`,
- wykrywanie wzorców klawiatury, np. `qwerty`, `asdf`, `zxcv`,
- wykrywanie lat, np. `1999`, `2024`, `2026`,
- wykrywanie prostych zamian typu leetspeak, np. `P@ssw0rd`,
- generowanie haseł z opcjami dla cyfr, znaków specjalnych i mylących znaków,
- porównywanie dwóch haseł,
- historia analiz bez zapisywania jawnych haseł,
- limit historii do ostatnich 20 analiz,
- prosty frontend w katalogu `frontend`,
- testy automatyczne i lintowanie przez Ruff.

## Technologie

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- Ruff
- HTML, CSS, JavaScript

## Uruchomienie

Utwórz i aktywuj środowisko:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
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

Frontend można uruchomić z drugiego terminala:

```powershell
cd frontend
python -m http.server 5500
```

Następnie otwórz:

```text
http://127.0.0.1:5500
```

## Endpointy

| Metoda | Endpoint | Opis |
| ------ | -------- | ---- |
| GET | `/api/` | Sprawdzenie, czy API działa |
| POST | `/api/analyze` | Analiza jednego hasła |
| GET | `/api/generate?length=16` | Wygenerowanie hasła |
| GET | `/api/generate?length=16&include_numbers=false&include_symbols=false&avoid_ambiguous=true` | Wygenerowanie hasła z opcjami |
| GET | `/api/tips` | Proste porady dotyczące haseł |
| GET | `/api/history` | Historia analiz |
| POST | `/api/compare` | Porównanie dwóch haseł |

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

## Testy i jakość kodu

Uruchom testy:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Uruchom Ruff:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Ruff sprawdza styl kodu, importy i częste błędy. GitHub Actions uruchamia Ruffa i testy po `push` oraz przy `pull_request`.

## Struktura

```text
app/
  api/
    routes.py
  data/
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
  test_history.py
```

## English

Password Security Analyzer API is a small FastAPI project for checking password strength. It scores a password from 0 to 100, estimates entropy, returns issues and suggestions, generates secure random passwords, compares two passwords and keeps analysis history without storing raw passwords.

This README was prepared and updated with help from Codex.
