from fastapi import APIRouter, HTTPException

from app.models.schemas import ComparePasswordsRequest, PasswordRequest
from app.services.analyzer import analyze_password
from app.services.generator import generate_password
from app.services.history import get_history, save_analysis


router = APIRouter()


@router.get("/")
def root():
    """Simple API health check."""
    return {"message": "Password Security Analyzer API is running"}


@router.post("/analyze")
def analyze(request: PasswordRequest):
    if not request.password.strip():
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty."
        )

    analysis = analyze_password(request.password)

    # PL: Historia zapisuje tylko metadane analizy, bez jawnej wartosci hasla.
    # EN: History stores only analysis metadata, not the raw password value.
    save_analysis(request.password, analysis)

    return analysis


@router.get("/generate")
def generate(length: int = 16):
    try:
        return {"password": generate_password(length)}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/tips")
def get_tips():
    """Return a short list of password safety tips."""
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
    """Return previous analyses without storing raw passwords."""
    return {"history": get_history()}


@router.post("/compare")
def compare_passwords(request: ComparePasswordsRequest):
    if not request.first_password.strip() or not request.second_password.strip():
        raise HTTPException(
            status_code=400,
            detail="Both passwords must be provided."
        )

    first_analysis = analyze_password(request.first_password)
    second_analysis = analyze_password(request.second_password)

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
