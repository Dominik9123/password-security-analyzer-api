import math
import re
import string
from datetime import datetime

WEAK_PASSWORDS_FILE = "app/data/weak_passwords.txt"


def load_weak_passwords() -> list:
    try:
        with open(WEAK_PASSWORDS_FILE) as file:
            return [line.strip().lower() for line in file if line.strip()]
    except FileNotFoundError:
        # Keep the analyzer usable even when the optional weak-password list is missing.
        return []


def calculate_entropy(password: str) -> float:
    charset_size = 0

    # Estimate entropy from the character groups present in the password.
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


def contains_sequence(password: str, sequence_length: int = 4) -> bool:
    lowered_password = password.lower()

    sequence_sources = [
        string.ascii_lowercase,
        string.ascii_lowercase[::-1],
        string.digits,
        string.digits[::-1],
    ]

    for source in sequence_sources:
        for index in range(len(source) - sequence_length + 1):
            sequence = source[index:index + sequence_length]

            if sequence in lowered_password:
                return True

    return False


def contains_keyboard_pattern(password: str) -> bool:
    lowered_password = password.lower()

    keyboard_patterns = [
        "qwerty",
        "asdf",
        "zxcv",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
    ]

    for pattern in keyboard_patterns:
        if pattern in lowered_password or pattern[::-1] in lowered_password:
            return True

    return False


def contains_year_pattern(password: str) -> bool:
    current_year = datetime.now().year
    years = re.findall(r"(?:19|20)\d{2}", password)

    for year in years:
        year_number = int(year)

        if 1900 <= year_number <= current_year + 1:
            return True

    return False


def normalize_leetspeak(password: str) -> str:
    replacements = str.maketrans({
        "0": "o",
        "1": "i",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
        "@": "a",
        "$": "s",
        "!": "i",
    })

    return password.lower().translate(replacements)


def contains_leetspeak_weak_word(password: str) -> bool:
    normalized_password = normalize_leetspeak(password)
    weak_passwords = load_weak_passwords()

    for weak_password in weak_passwords:
        if weak_password in normalized_password:
            return True

    return False


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

    # Keep common weak patterns data-driven so the list can grow without code changes.
    for weak_password in weak_passwords:
        if weak_password in lowered_password:
            score -= 20
            issues.append(
                f"Password contains common pattern: {weak_password}."
            )
            suggestions.append("Avoid common words and sequences.")
            break

    if re.search(r"(.)\1{2,}", password):
        # Flag three or more identical characters in a row.
        score -= 10
        issues.append("Password contains repeated characters.")
        suggestions.append("Avoid repeated characters like aaa or 111.")

    if contains_sequence(password):
        score -= 10
        issues.append("Password contains a predictable sequence.")
        suggestions.append("Avoid sequences like abcd or 1234.")

    if contains_keyboard_pattern(password):
        score -= 10
        issues.append("Password contains a common keyboard pattern.")
        suggestions.append("Avoid keyboard patterns like qwerty or asdf.")

    if contains_year_pattern(password):
        score -= 10
        issues.append("Password contains a year-like pattern.")
        suggestions.append("Avoid using years, birthdays, or anniversaries.")

    if contains_leetspeak_weak_word(password):
        score -= 10
        issues.append(
            "Password contains a weak word with common substitutions.")
        suggestions.append(
            "Avoid predictable substitutions like @ for a or 0 for o.")

    entropy = calculate_entropy(password)

    # Combine composition rules, entropy, and penalties into the final score.
    if entropy >= 60:
        score += 20
    elif entropy >= 40:
        score += 10
    else:
        issues.append("Password entropy is low.")
        suggestions.append("Use a longer and more diverse password.")

    # Keep the public score on a predictable 0-100 scale.
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
