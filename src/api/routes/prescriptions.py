import base64
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.prescriptions.parser import parse_image
from src.prescriptions.explainer import explain_prescription

router = APIRouter()


class ExplainResponse(BaseModel):
    original_text: str
    explanation: str
    language: str
    medications: list[str]
    warnings: list[str]
    disclaimer: str


@router.post("/explain", response_model=ExplainResponse)
async def explain(
    image: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
):
    if image:
        raw_bytes = await image.read()
        extracted_text = parse_image(raw_bytes)
    elif text:
        extracted_text = text
    else:
        raise HTTPException(status_code=400, detail="Provide either image or text")

    result = await explain_prescription(extracted_text, language)
    return result
