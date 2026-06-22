import logging

logger = logging.getLogger(__name__)

MAX_TEXT_LENGTH = 10_000
MIN_TEXT_LENGTH = 5


def validate_prescription_text(text: str) -> None:
    if len(text) < MIN_TEXT_LENGTH:
        raise ValueError("Prescription text too short to process")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"Prescription text exceeds maximum length of {MAX_TEXT_LENGTH} characters")
