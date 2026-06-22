import pytest
from src.core.safety import validate_output, append_disclaimer


def test_disclaimer_appended():
    result = append_disclaimer("Take one tablet daily.", "en")
    assert "guidance only" in result.lower()
    assert "pharmacist" in result.lower()


def test_diagnostic_claim_blocked():
    ok, reason = validate_output("You have diabetes based on your symptoms.")
    assert not ok


def test_dose_change_blocked():
    ok, reason = validate_output("You should increase your dose to 10mg.")
    assert not ok


def test_safe_output_passes():
    ok, _ = validate_output("This medication helps manage blood pressure.")
    assert ok


def test_disclaimer_in_urdu():
    result = append_disclaimer("روزانہ ایک گولی لیں۔", "ur")
    assert "فارماسسٹ" in result


def test_disclaimer_fallback_to_english():
    result = append_disclaimer("Take daily.", "xx")
    assert "pharmacist" in result.lower()
