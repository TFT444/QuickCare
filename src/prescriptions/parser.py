import io
import logging
import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)


def parse_image(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image, lang="eng")
        cleaned = " ".join(text.split())
        logger.info("OCR extracted %d chars", len(cleaned))
        return cleaned
    except Exception as exc:
        logger.error("OCR failed: %s", exc)
        raise ValueError(f"Could not extract text from image: {exc}") from exc
