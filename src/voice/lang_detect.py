import logging
from langdetect import detect, LangDetectException

logger = logging.getLogger(__name__)

_NHS_SUPPORTED = {"en", "ur", "bn", "so", "pl", "ar", "pa", "ta", "ro", "gu"}


def detect_language(text: str) -> str:
    if not text or len(text.strip()) < 10:
        return "en"
    try:
        lang = detect(text)
        if lang not in _NHS_SUPPORTED:
            logger.info("Detected unsupported language '%s', defaulting to 'en'", lang)
            return "en"
        return lang
    except LangDetectException:
        logger.warning("Language detection failed, defaulting to 'en'")
        return "en"
