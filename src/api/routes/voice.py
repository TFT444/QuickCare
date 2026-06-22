from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.voice.stt import transcribe_audio
from src.voice.tts import synthesise_speech

router = APIRouter()


class TranscribeResponse(BaseModel):
    transcript: str
    language: str


class SpeakResponse(BaseModel):
    audio_url: str
    language: str


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(audio: UploadFile = File(...)):
    raw_bytes = await audio.read()
    result = await transcribe_audio(raw_bytes, audio.filename or "audio.wav")
    return result


@router.post("/speak", response_model=SpeakResponse)
async def speak(
    text: str = Form(...),
    language: str = Form("en"),
):
    result = await synthesise_speech(text, language)
    return result
