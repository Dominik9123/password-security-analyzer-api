from app.services.analyzer import analyze_password, calculate_entropy


def test_strong_password_has_high_score():
    """A strong password should receive a high score."""
    result = analyze_password("Xy9!Lm2@Qz7#Rt5$")

    assert result["score"] >= 80
    assert result["strength"] == "strong"


def test_weak_password_has_low_score():
    """A common digit sequence should be rated as weak."""
    result = analyze_password("123456")

    assert result["score"] < 50
    assert result["strength"] == "weak"


def test_password_without_special_character_has_issue():
    """Missing punctuation should be reported as an issue."""
    result = analyze_password("Password123456")

    assert "Password has no special characters." in result["issues"]


def test_entropy_returns_float():
    """Entropy should be a positive float value."""
    entropy = calculate_entropy("Password123!")

    assert isinstance(entropy, float)
    assert entropy > 0


def test_password_with_digit_sequence_has_issue():
    result = analyze_password("Password1234!")

    assert "Password contains a predictable sequence." in result["issues"]


def test_password_with_letter_sequence_has_issue():
    result = analyze_password("AbcdPassword123!")

    assert "Password contains a predictable sequence." in result["issues"]


def test_password_with_reversed_sequence_has_issue():
    result = analyze_password("Password9876!")

    assert "Password contains a predictable sequence." in result["issues"]


def test_password_with_keyboard_pattern_has_issue():
    result = analyze_password("QwertyPassword123!")

    assert "Password contains a common keyboard pattern." in result["issues"]


def test_password_with_reversed_keyboard_pattern_has_issue():
    result = analyze_password("PasswordYtrewq123!")

    assert "Password contains a common keyboard pattern." in result["issues"]


def test_password_with_year_pattern_has_issue():
    result = analyze_password("Password2024!")

    assert "Password contains a year-like pattern." in result["issues"]


def test_password_with_future_year_outside_range_has_no_year_issue():
    result = analyze_password("Password2099!")

    assert "Password contains a year-like pattern." not in result["issues"]


def test_password_with_non_first_keyboard_pattern_has_issue():
    result = analyze_password("AsdfPassword123!")

    assert "Password contains a common keyboard pattern." in result["issues"]


def test_password_with_leetspeak_weak_word_has_issue():
    result = analyze_password("P@ssw0rd123!")

    assert (
        "Password contains a weak word with common substitutions."
        in result["issues"]
    )
