import random
import string


def generate_password(length: int = 16) -> str:
    """PL: Generuje losowe hasło z liter, cyfr i znaków specjalnych.
    EN: Generates a random password using letters, digits, and punctuation characters.
    """

    # PL: Minimalna długość chroni przed generowaniem haseł zbyt łatwych do złamania.
    # EN: Minimum length prevents generating passwords that are too easy to crack.
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    # PL: Pełny zestaw znaków zwiększa różnorodność oraz potencjalną entropię hasła.
    # EN: Full character set increases password diversity and potential entropy.
    characters = string.ascii_letters + string.digits + string.punctuation

    return "".join(random.choice(characters) for _ in range(length))
