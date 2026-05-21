import secrets
import string

AMBIGUOUS_CHARACTERS = "O0Il1"


def remove_ambiguous_characters(characters: str) -> str:
    return "".join(char for char in characters if char not in AMBIGUOUS_CHARACTERS)


def generate_password(
    length: int = 16,
    include_numbers: bool = True,
    include_symbols: bool = True,
    avoid_ambiguous: bool = False,
) -> str:
    """Generate a cryptographically secure password."""
    if length < 8:
        raise ValueError("Password length must be at least 8 characters")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation

    if avoid_ambiguous:
        lowercase = remove_ambiguous_characters(lowercase)
        uppercase = remove_ambiguous_characters(uppercase)
        digits = remove_ambiguous_characters(digits)

    required_groups = [lowercase, uppercase]

    if include_numbers:
        required_groups.append(digits)

    if include_symbols:
        required_groups.append(punctuation)

    if length < len(required_groups):
        raise ValueError(
            "Password length is too short for the selected options")

    all_characters = "".join(required_groups)

    required_characters = [
        secrets.choice(group)
        for group in required_groups
    ]

    remaining_length = length - len(required_characters)

    password_characters = required_characters + [
        secrets.choice(all_characters)
        for _ in range(remaining_length)
    ]

    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)
