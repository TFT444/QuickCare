import pytest
from src.prescriptions.validator import validate_prescription_text


def test_valid_text():
    validate_prescription_text("Amoxicillin 500mg — take one capsule three times daily for 7 days.")


def test_too_short():
    with pytest.raises(ValueError, match="too short"):
        validate_prescription_text("Hi")


def test_too_long():
    with pytest.raises(ValueError, match="maximum length"):
        validate_prescription_text("a" * 10_001)
