import logging
import re
from src.core.ai_engine import explain_prescription as ai_explain
from src.core.safety import safe_output
from src.prescriptions.validator import validate_prescription_text
from src.voice.lang_detect import detect_language

logger = logging.getLogger(__name__)

_MEDICATION_PATTERN = re.compile(
    r"\b([A-Z][a-z]+(?:mycin|cillin|olol|pril|artan|statin|mab|nib|pam|zam|zole|pine|dine|ine|ate|ide|ium)?)\b"
)


def _extract_medications(text: str) -> list[str]:
    return list({m.group(1) for m in _MEDICATION_PATTERN.finditer(text)})


async def explain_prescription(raw_text: str, language: str | None) -> dict:
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty prescription text")

    validate_prescription_text(raw_text)

    detected_lang = language or detect_language(raw_text)
    explanation = await ai_explain(raw_text, detected_lang)
    safe = safe_output(explanation, detected_lang)

    medications = _extract_medications(raw_text)
    warnings: list[str] = []
    if len(medications) > 3:
        warnings.append("Multiple medications detected — ask your pharmacist about interactions.")

    disclaimer_line = safe.split("\n---\n")[-1] if "\n---\n" in safe else ""
    explanation_body = safe.split("\n---\n")[0] if "\n---\n" in safe else safe

    return {
        "original_text": raw_text,
        "explanation": explanation_body,
        "language": detected_lang,
        "medications": medications,
        "warnings": warnings,
        "disclaimer": disclaimer_line,
    }
