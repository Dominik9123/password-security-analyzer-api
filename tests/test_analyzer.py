from app.services.analyzer import analyze_password, calculate_entropy


def test_strong_password_has_high_score():
    """PL: Silne hasło powinno uzyskać wysoki wynik. EN: A strong password should receive a high score."""
    result = analyze_password("Xy9!Lm2@Qz7#Rt5$")

    assert result["score"] >= 80
    assert result["strength"] == "strong"


def test_weak_password_has_low_score():
    """PL: Popularna sekwencja cyfr powinna zostać oceniona jako słaba. EN: A common digit sequence should be weak."""
    result = analyze_password("123456")

    assert result["score"] < 50
    assert result["strength"] == "weak"


def test_password_without_special_character_has_issue():
    """PL: Brak znaku specjalnego powinien pojawić się na liście problemów. EN: Missing punctuation should be reported."""
    result = analyze_password("Password123456")

    assert "Password has no special characters." in result["issues"]


def test_entropy_returns_float():
    """PL: Entropia powinna być dodatnią liczbą zmiennoprzecinkową. EN: Entropy should be a positive float value."""
    entropy = calculate_entropy("Password123!")

    assert isinstance(entropy, float)
    assert entropy > 0
