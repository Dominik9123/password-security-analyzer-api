import string

import pytest

from app.services.generator import generate_password


def test_generate_password_default_length():
    """The default generated password length should be 16 characters."""
    password = generate_password()

    assert len(password) == 16


def test_generate_password_custom_length():
    """The generator should support a custom password length."""
    password = generate_password(20)

    assert len(password) == 20


def test_generate_password_minimum_length_error():
    """Too short a password length should raise an error."""
    with pytest.raises(ValueError):
        generate_password(5)


def test_generate_password_contains_required_character_types():
    """Generated passwords should include all required character groups."""
    password = generate_password(16)

    assert any(char.islower() for char in password)
    assert any(char.isupper() for char in password)
    assert any(char.isdigit() for char in password)
    assert any(char in string.punctuation for char in password)


def test_generate_password_can_exclude_numbers():
    password = generate_password(include_numbers=False)

    assert not any(char.isdigit() for char in password)


def test_generate_password_can_exclude_symbols():
    password = generate_password(include_symbols=False)

    assert not any(char in string.punctuation for char in password)


def test_generate_password_can_avoid_ambiguous_characters():
    password = generate_password(length=64, avoid_ambiguous=True)

    assert not any(char in "O0Il1" for char in password)
