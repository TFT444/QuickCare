import os
import logging
import tempfile
import azure.cognitiveservices.speech as speechsdk

logger = logging.getLogger(__name__)

VOICE_MAP: dict[str, str] = {
    "en": "en-GB-SoniaNeural",
    "ur": "ur-PK-UzmaNeural",
    "bn": "bn-BD-NabanitaNeural",
    "ar": "ar-SA-ZariyahNeural",
    "pl": "pl-PL-ZofiaNeural",
    "so": "en-GB-SoniaNeural",  # fallback — no Somali Azure voice
    "pa": "pa-IN-OjasNeural",
    "ta": "ta-IN-PallaviNeural",
    "ro": "ro-RO-AlinaNeural",
    "gu": "gu-IN-DhwaniNeural",
}


async def synthesise_speech(text: str, language: str) -> dict:
    key = os.environ.get("AZURE_TTS_KEY", "")
    region = os.environ.get("AZURE_TTS_REGION", "uksouth")

    if not key:
        logger.warning("AZURE_TTS_KEY not set — returning stub audio path")
        return {"audio_url": "/static/audio/stub.mp3", "language": language}

    voice = VOICE_MAP.get(language, "en-GB-SoniaNeural")
    config = speechsdk.SpeechConfig(subscription=key, region=region)
    config.speech_synthesis_voice_name = voice

    tmp_path = tempfile.mktemp(suffix=".mp3")
    audio_config = speechsdk.audio.AudioOutputConfig(filename=tmp_path)
    synthesiser = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=audio_config)

    result = synthesiser.speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        logger.error("TTS failed: %s", result.cancellation_details)
        return {"audio_url": "/static/audio/error.mp3", "language": language}

    audio_filename = os.path.basename(tmp_path)
    return {"audio_url": f"/static/audio/{audio_filename}", "language": language}
