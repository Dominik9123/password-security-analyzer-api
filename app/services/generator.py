import random
import string


def generate_password(length: int = 16) -> str:
    """Generate a random password from letters, digits and symbols."""
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    # PL: Uzywamy pelnego zestawu znakow, zeby wygenerowane haslo bylo roznorodne.
    # EN: The full character set keeps generated passwords varied.
    characters = string.ascii_letters + string.digits + string.punctuation

    return "".join(random.choice(characters) for _ in range(length))
