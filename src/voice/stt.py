import os
import logging
import tempfile
from pathlib import Path
import openai

from src.voice.lang_detect import detect_language

logger = logging.getLogger(__name__)

_client: openai.OpenAI | None = None


def _get_client() -> openai.OpenAI:
    global _client
    if _client is None:
        _client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    return _client


async def transcribe_audio(audio_bytes: bytes, filename: str) -> dict:
    suffix = Path(filename).suffix or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        client = _get_client()
        with open(tmp_path, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
            )
        transcript = response.text
        detected_language = getattr(response, "language", None) or detect_language(transcript)
    finally:
        os.unlink(tmp_path)

    logger.info("Transcribed audio — language: %s chars: %d", detected_language, len(transcript))
    return {"transcript": transcript, "language": detected_language}
