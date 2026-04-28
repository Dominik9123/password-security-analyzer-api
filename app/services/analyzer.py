import math
import re
import string


WEAK_PASSWORDS_FILE = "app/data/weak_passwords.txt"


def load_weak_passwords() -> list:
    try:
        with open(WEAK_PASSWORDS_FILE, "r") as file:
            return [line.strip().lower() for line in file if line.strip()]
    except FileNotFoundError:
        return []


def calculate_entropy(password: str) -> float:
    charset_size = 0

    # PL: Entropia jest liczona z przyblizonego zestawu znakow uzytych w hasle.
    # EN: Entropy is based on the estimated character set used by the password.
    if any(char.islower() for char in password):
        charset_size += 26

    if any(char.isupper() for char in password):
        charset_size += 26

    if any(char.isdigit() for char in password):
        charset_size += 10

    if any(char in string.punctuation for char in password):
        charset_size += len(string.punctuation)

    if charset_size == 0:
        return 0.0

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)


def analyze_password(password: str) -> dict:
    score = 0
    issues = []
    suggestions = []

    if len(password) >= 12:
        score += 25
    else:
        issues.append("Password is shorter than 12 characters.")
        suggestions.append("Use at least 12 characters.")

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
    weak_passwords = load_weak_passwords()

    # PL: Lista z pliku pozwala rozszerzac slabe wzorce bez zmiany kodu.
    # EN: The file-based list lets us add weak patterns without changing code.
    for weak_password in weak_passwords:
        if weak_password in lowered_password:
            score -= 20
            issues.append(
                f"Password contains common pattern: {weak_password}."
            )
            suggestions.append("Avoid common words and sequences.")
            break

    if re.search(r"(.)\1{2,}", password):
        score -= 10
        issues.append("Password contains repeated characters.")
        suggestions.append("Avoid repeated characters like aaa or 111.")

    entropy = calculate_entropy(password)

    # PL: Koncowa ocena laczy reguly znakow z entropia i karami za proste wzorce.
    # EN: The final score combines character rules, entropy and weak-pattern penalties.
    if entropy >= 60:
        score += 20
    elif entropy >= 40:
        score += 10
    else:
        issues.append("Password entropy is low.")
        suggestions.append("Use a longer and more diverse password.")

    score = max(0, min(score, 100))

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
