# Password Security Analyzer API

## Polski

### Opis projektu

Password Security Analyzer API to aplikacja backendowa napisana w Pythonie z użyciem FastAPI. Projekt umożliwia analizę siły hasła, obliczanie jego entropii, wykrywanie typowych słabości, generowanie bezpiecznych haseł, porównywanie dwóch haseł oraz zapisywanie historii analiz bez przechowywania jawnych wartości haseł.

Projekt jest przygotowany w sposób odpowiedni do prezentacji akademickiej: posiada wydzieloną strukturę aplikacji, modele danych, warstwę serwisową, endpointy API, automatyczną dokumentację Swagger oraz testy jednostkowe i integracyjne.

### Funkcjonalności

- Analiza siły hasła w skali 0-100.
- Klasyfikacja hasła jako `weak`, `medium` lub `strong`.
- Obliczanie entropii hasła na podstawie długości i zestawu znaków.
- Wykrywanie braku małych liter, wielkich liter, cyfr i znaków specjalnych.
- Wykrywanie popularnych wzorców, takich jak `123456`, `password`, `qwerty`, `admin`.
- Wykrywanie powtarzających się znaków za pomocą wyrażeń regularnych.
- Generowanie losowych haseł o zadanej długości.
- Porównywanie dwóch haseł i wskazywanie silniejszego.
- Zwracanie porad dotyczących tworzenia bezpiecznych haseł.
- Zapisywanie historii analiz bez zapisywania oryginalnych haseł.

### Technologie

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTTPX / FastAPI TestClient
- JSON
- Wyrażenia regularne (`re`)

### Instalacja i uruchomienie

1. Sklonuj lub otwórz katalog projektu.

2. Utwórz i aktywuj środowisko wirtualne:

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

3. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

4. Uruchom aplikację:

```bash
uvicorn app.main:app --reload
```

5. Otwórz API w przeglądarce:

```text
http://127.0.0.1:8000/api/
```

### Struktura projektu

```text
Password-Security-Analyzer-API/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── data/
│   │   ├── history.json
│   │   └── weak_passwords.txt
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── analyzer.py
│   │   ├── generator.py
│   │   └── history.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_api.py
│   ├── test_generator.py
│   └── __init__.py
├── pytest.ini
├── requirements.txt
└── README.md
```

### Endpointy API

| Metoda | Endpoint                  | Opis                               |
| ------ | ------------------------- | ---------------------------------- |
| GET    | `/api/`                   | Sprawdza, czy API działa.          |
| POST   | `/api/analyze`            | Analizuje siłę jednego hasła.      |
| GET    | `/api/generate?length=16` | Generuje losowe hasło.             |
| GET    | `/api/tips`               | Zwraca porady dotyczące haseł.     |
| GET    | `/api/history`            | Zwraca historię wykonanych analiz. |
| POST   | `/api/compare`            | Porównuje dwa hasła.               |

### Dokumentacja Swagger

FastAPI automatycznie generuje interaktywną dokumentację API. Po uruchomieniu aplikacji dokumentacja jest dostępna pod adresem:

```text
http://127.0.0.1:8000/docs
```

Alternatywna dokumentacja ReDoc:

```text
http://127.0.0.1:8000/redoc
```

### Przykładowe żądania i odpowiedzi

#### Analiza hasła

Request:

```http
POST /api/analyze
Content-Type: application/json
```

```json
{
  "password": "StrongPassword123!"
}
```

Response:

```json
{
  "score": 90,
  "strength": "strong",
  "entropy": 104.92,
  "issues": [],
  "suggestions": []
}
```

#### Generowanie hasła

Request:

```http
GET /api/generate?length=20
```

Response:

```json
{
  "password": "A8!kL2#pQ9@zRt5$xM1?"
}
```

#### Porównanie haseł

Request:

```http
POST /api/compare
Content-Type: application/json
```

```json
{
  "first_password": "test123",
  "second_password": "StrongPassword123!"
}
```

Response:

```json
{
  "first_password": {
    "score": 10,
    "strength": "weak",
    "entropy": 36.19,
    "issues": [
      "Password is shorter than 12 characters.",
      "Password has no uppercase letters.",
      "Password has no special characters.",
      "Password entropy is low."
    ],
    "suggestions": [
      "Use at least 12 characters.",
      "Add uppercase letters.",
      "Add special characters.",
      "Use a longer and more diverse password."
    ]
  },
  "second_password": {
    "score": 90,
    "strength": "strong",
    "entropy": 104.92,
    "issues": [],
    "suggestions": []
  },
  "stronger_password": "second_password"
}
```

### Punktacja hasła

System punktacji uwzględnia:

- długość hasła,
- obecność małych liter,
- obecność wielkich liter,
- obecność cyfr,
- obecność znaków specjalnych,
- entropię,
- kary za popularne wzorce,
- kary za powtarzające się znaki.

Entropia jest liczona według wzoru:

```text
entropy = password_length * log2(character_set_size)
```

Im dłuższe hasło i im większa różnorodność znaków, tym wyższa entropia oraz trudność złamania hasła metodą brute force.

### Testowanie

Uruchom wszystkie testy:

```bash
pytest
```

Testy obejmują:

- analizę silnych i słabych haseł,
- obliczanie entropii,
- generowanie haseł,
- obsługę minimalnej długości hasła,
- działanie głównych endpointów API,
- porównywanie haseł.

### Możliwe przyszłe usprawnienia

- Dodanie autoryzacji użytkowników.
- Zastąpienie pliku JSON bazą danych, np. SQLite lub PostgreSQL.
- Dodanie rate limitingu dla endpointów API.
- Rozbudowanie listy słabych haseł.
- Integracja z bazą wycieków haseł, np. Have I Been Pwned API.
- Dodanie konteneryzacji Docker.
- Dodanie pipeline CI/CD.
- Dodanie bardziej zaawansowanego algorytmu oceny haseł.

## English

### Project Overview

Password Security Analyzer API is a Python backend application built with FastAPI. The project analyzes password strength, calculates entropy, detects common weaknesses, generates secure passwords, compares two passwords, and stores analysis history without saving raw password values.

The project is suitable for academic submission because it includes a clear application structure, data models, service layer, API endpoints, automatically generated Swagger documentation, and automated unit/integration tests.

### Features

- Password strength analysis on a 0-100 scale.
- Password classification as `weak`, `medium`, or `strong`.
- Entropy calculation based on password length and character set size.
- Detection of missing lowercase letters, uppercase letters, digits, and special characters.
- Detection of common patterns such as `123456`, `password`, `qwerty`, and `admin`.
- Detection of repeated characters using regular expressions.
- Random password generation with configurable length.
- Comparison of two passwords and selection of the stronger one.
- Security tips for creating stronger passwords.
- Analysis history stored without raw password values.

### Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTTPX / FastAPI TestClient
- JSON
- Regular expressions (`re`)

### Installation Guide

1. Clone or open the project directory.

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
uvicorn app.main:app --reload
```

5. Open the API in a browser:

```text
http://127.0.0.1:8000/api/
```

### Project Structure

```text
Password-Security-Analyzer-API/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── data/
│   │   ├── history.json
│   │   └── weak_passwords.txt
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── analyzer.py
│   │   ├── generator.py
│   │   └── history.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_api.py
│   ├── test_generator.py
│   └── __init__.py
├── pytest.ini
├── requirements.txt
└── README.md
```

### API Endpoints

| Method | Endpoint                  | Description                        |
| ------ | ------------------------- | ---------------------------------- |
| GET    | `/api/`                   | Checks whether the API is running. |
| POST   | `/api/analyze`            | Analyzes a single password.        |
| GET    | `/api/generate?length=16` | Generates a random password.       |
| GET    | `/api/tips`               | Returns password security tips.    |
| GET    | `/api/history`            | Returns saved analysis history.    |
| POST   | `/api/compare`            | Compares two passwords.            |

### Swagger Documentation

FastAPI automatically generates interactive API documentation. After starting the application, Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

### Example Requests and Responses

#### Password Analysis

Request:

```http
POST /api/analyze
Content-Type: application/json
```

```json
{
  "password": "StrongPassword123!"
}
```

Response:

```json
{
  "score": 90,
  "strength": "strong",
  "entropy": 104.92,
  "issues": [],
  "suggestions": []
}
```

#### Password Generation

Request:

```http
GET /api/generate?length=20
```

Response:

```json
{
  "password": "A8!kL2#pQ9@zRt5$xM1?"
}
```

#### Password Comparison

Request:

```http
POST /api/compare
Content-Type: application/json
```

```json
{
  "first_password": "test123",
  "second_password": "StrongPassword123!"
}
```

Response:

```json
{
  "first_password": {
    "score": 10,
    "strength": "weak",
    "entropy": 36.19,
    "issues": [
      "Password is shorter than 12 characters.",
      "Password has no uppercase letters.",
      "Password has no special characters.",
      "Password entropy is low."
    ],
    "suggestions": [
      "Use at least 12 characters.",
      "Add uppercase letters.",
      "Add special characters.",
      "Use a longer and more diverse password."
    ]
  },
  "second_password": {
    "score": 90,
    "strength": "strong",
    "entropy": 104.92,
    "issues": [],
    "suggestions": []
  },
  "stronger_password": "second_password"
}
```

### Password Scoring

The scoring system considers:

- password length,
- lowercase letters,
- uppercase letters,
- digits,
- special characters,
- entropy,
- penalties for common patterns,
- penalties for repeated characters.

Entropy is calculated using:

```text
entropy = password_length * log2(character_set_size)
```

The longer and more diverse the password is, the higher its entropy and resistance to brute-force attacks.

### Testing Instructions

Run all tests:

```bash
pytest
```

The test suite covers:

- strong and weak password analysis,
- entropy calculation,
- password generation,
- minimum password length validation,
- main API endpoints,
- password comparison.

### Future Improvements

- Add user authentication.
- Replace JSON file storage with a database such as SQLite or PostgreSQL.
- Add API rate limiting.
- Expand the weak password pattern list.
- Integrate with breach databases, for example Have I Been Pwned API.
- Add Docker containerization.
- Add a CI/CD pipeline.
- Add a more advanced password scoring algorithm.
