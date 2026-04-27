import re
import math
import string

# PL: Lista prostych, często spotykanych wzorców obniżających bezpieczeństwo hasła.
# EN: List of simple, commonly used patterns that reduce password security.
COMMON_PATTERNS = ["123456", "password", "qwerty", "admin", "abcdef"]


def calculate_entropy(password: str) -> float:
    """PL: Oblicza entropię hasła na podstawie długości i rozmiaru zestawu znaków.
    EN: Calculates password entropy using password length and estimated character set size.

    PL: Wzór: entropy = length * log2(charset_size).
    EN: Formula: entropy = length * log2(charset_size).
    """
    charset_size = 0

    # PL/EN: Każda wykryta grupa znaków zwiększa teoretyczną przestrzeń wyszukiwania.
    if any(char.islower() for char in password):
        charset_size += 26

    if any(char.isupper() for char in password):
        charset_size += 26

    if any(char.isdigit() for char in password):
        charset_size += 10

    if any(char in string.punctuation for char in password):
        charset_size += len(string.punctuation)

    # PL: Brak rozpoznanego zestawu znaków oznacza brak mierzalnej entropii.
    # EN: No recognized character set means no measurable entropy.
    if charset_size == 0:
        return 0.0

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)


def analyze_password(password: str) -> dict:
    """PL: Analizuje hasło i zwraca ocenę, siłę, entropię, problemy oraz sugestie.
    EN: Analyzes a password and returns score, strength, entropy, issues, and suggestions.

    PL: Wynik jest sumą punktów za długość, różnorodność znaków i entropię,
    z karami za popularne wzorce oraz powtarzające się znaki.
    EN: The score combines length, character diversity, and entropy points,
    with penalties for common patterns and repeated characters.
    """
    score = 0
    issues = []
    suggestions = []

    # PL: Długość hasła jest podstawowym czynnikiem bezpieczeństwa.
    # EN: Password length is a primary security factor.
    if len(password) >= 12:
        score += 25
    else:
        issues.append("Password is shorter than 12 characters.")
        suggestions.append("Use at least 12 characters.")

    # PL: Reguły różnorodności znaków premiują małe litery, wielkie litery, cyfry i znaki specjalne.
    # EN: Character diversity rules reward lowercase letters, uppercase letters, digits, and special characters.
    if any(char.islower() for char in password):
        score += 10
    else:
        issues.append("Password has no lowercase letters.")
        suggestions.append("Add lowercase letters.")

    if any(char.isupper() for char in password):
        score += 10
    else:
        issues.append("Password has no uppercase letters.")
        suggestions.append("Add uppercase letters.")

    if any(char.isdigit() for char in password):
        score += 10
    else:
        issues.append("Password has no numbers.")
        suggestions.append("Add numbers.")

    if any(char in string.punctuation for char in password):
        score += 15
    else:
        issues.append("Password has no special characters.")
        suggestions.append("Add special characters.")

    lowered_password = password.lower()

    # PL: Popularne frazy i sekwencje są łatwe do odgadnięcia, więc obniżają wynik.
    # EN: Common words and sequences are easy to guess, so they lower the score.
    for pattern in COMMON_PATTERNS:
        if pattern in lowered_password:
            score -= 20
            issues.append(f"Password contains common pattern: {pattern}.")
            suggestions.append("Avoid common words and sequences.")
            break

    # PL: Regex (.)\1{2,} wykrywa co najmniej trzy takie same znaki pod rząd, np. aaa lub 111.
    # EN: Regex (.)\1{2,} detects at least three identical consecutive characters, e.g. aaa or 111.
    if re.search(r"(.)\1{2,}", password):
        score -= 10
        issues.append("Password contains repeated characters.")
        suggestions.append("Avoid repeated characters like aaa or 111.")

    entropy = calculate_entropy(password)

    # PL: Wyższa entropia oznacza większą liczbę możliwych kombinacji do sprawdzenia.
    # EN: Higher entropy means a larger number of possible combinations to brute-force.
    if entropy >= 60:
        score += 20
    elif entropy >= 40:
        score += 10
    else:
        issues.append("Password entropy is low.")
        suggestions.append("Use a longer and more diverse password.")

    # PL: Wynik końcowy jest ograniczony do zakresu 0-100 dla czytelnej interpretacji.
    # EN: Final score is clamped to the 0-100 range for clear interpretation.
    score = max(0, min(score, 100))

    # PL: Kategorie siły hasła są wyprowadzane z końcowego wyniku punktowego.
    # EN: Password strength categories are derived from the final numeric score.
    if score >= 80:
        strength = "strong"
    elif score >= 50:
        strength = "medium"
    else:
        strength = "weak"

    return {
        "score": score,
        "strength": strength,
        "entropy": entropy,
        "issues": issues,
        "suggestions": list(set(suggestions))
    }
