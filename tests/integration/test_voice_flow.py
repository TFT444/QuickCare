import pytest
from unittest.mock import AsyncMock, patch
import asyncio


def test_transcribe_stub():
    with patch("src.voice.stt.transcribe_audio", new_callable=AsyncMock) as mock_stt:
        mock_stt.return_value = {"transcript": "I have a headache", "language": "en"}
        result = asyncio.run(mock_stt(b"audio", "test.wav"))
    assert result["language"] == "en"
    assert "transcript" in result


def test_speak_stub():
    with patch("src.voice.tts.synthesise_speech", new_callable=AsyncMock) as mock_tts:
        mock_tts.return_value = {"audio_url": "/static/audio/stub.mp3", "language": "ur"}
        result = asyncio.run(mock_tts("مرحبا", "ur"))
    assert result["language"] == "ur"
    assert "audio_url" in result
