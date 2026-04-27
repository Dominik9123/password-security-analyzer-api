from fastapi import APIRouter
from app.models.schemas import PasswordRequest, ComparePasswordsRequest
from app.services.analyzer import analyze_password
from app.services.generator import generate_password
from app.services.history import save_analysis, get_history

router = APIRouter()


@router.get("/")
def root():
    """PL: Endpoint kontrolny API. EN: Basic health/status endpoint."""
    return {"message": "Password Security Analyzer API is running"}


@router.post("/analyze")
def analyze(request: PasswordRequest):
    """PL: Analizuje siłę hasła i zapisuje wynik bez przechowywania hasła.
    EN: Analyzes password strength and stores the result without saving the password.
    """
    analysis = analyze_password(request.password)
    save_analysis(request.password, analysis)
    return analysis


@router.get("/generate")
def generate(length: int = 16):
    """PL: Generuje losowe hasło o podanej długości. EN: Generates a random password of the requested length."""
    return {"password": generate_password(length)}


@router.get("/tips")
def get_tips():
    """PL: Zwraca podstawowe zalecenia bezpieczeństwa haseł. EN: Returns basic password security tips."""
    return {
        "tips": [
            "Use at least 12 characters.",
            "Use lowercase and uppercase letters.",
            "Add numbers and special characters.",
            "Avoid common passwords like password123.",
            "Do not reuse passwords across websites."
        ]
    }


@router.get("/history")
def history():
    """PL: Zwraca historię analiz bez jawnych wartości haseł. EN: Returns analysis history without raw passwords."""
    return {"history": get_history()}


@router.post("/compare")
def compare_passwords(request: ComparePasswordsRequest):
    """PL: Porównuje dwa hasła na podstawie wyniku punktowego.
    EN: Compares two passwords using the calculated score.
    """
    first_analysis = analyze_password(request.first_password)
    second_analysis = analyze_password(request.second_password)

    # PL: Hasło z wyższym wynikiem jest uznawane za silniejsze.
    # EN: The password with the higher score is considered stronger.
    if first_analysis["score"] > second_analysis["score"]:
        stronger_password = "first_password"
    elif second_analysis["score"] > first_analysis["score"]:
        stronger_password = "second_password"
    else:
        stronger_password = "both_are_equal"

    return {
        "first_password": first_analysis,
        "second_password": second_analysis,
        "stronger_password": stronger_password
    }
