import pytest
from app.services.generator import generate_password


def test_generate_password_default_length():
    """PL: Domyślna długość generatora wynosi 16 znaków. EN: Default generator length is 16 characters."""
    password = generate_password()

    assert len(password) == 16


def test_generate_password_custom_length():
    """PL: Generator powinien obsługiwać własną długość. EN: Generator should support a custom length."""
    password = generate_password(20)

    assert len(password) == 20


def test_generate_password_minimum_length_error():
    """PL: Zbyt krótka długość powinna zgłosić błąd. EN: Too short length should raise an error."""
    with pytest.raises(ValueError):
        generate_password(5)
