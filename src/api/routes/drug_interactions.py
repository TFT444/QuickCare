from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.core import drug_checker
from src.core.safety import safe_output

router = APIRouter()


class DrugInteractionRequest(BaseModel):
    medications: list[str] = Field(..., min_length=1, description="List of medication names")
    language: str = Field(default="en", description="ISO 639-1 language code")


class DrugInteractionResponse(BaseModel):
    medications: list[str]
    guidance: str
    language: str
    disclaimer: str
    interactions_detected: bool


@router.post("/check", response_model=DrugInteractionResponse)
async def check_drug_interactions(body: DrugInteractionRequest):
    if not body.medications:
        raise HTTPException(status_code=422, detail="At least one medication is required.")

    result = await drug_checker.check(body.medications, body.language)

    raw_guidance = result.get("guidance", "")
    safe = safe_output(raw_guidance, body.language) if raw_guidance else ""

    disclaimer_start = safe.rfind("\n\n---")
    if disclaimer_start != -1:
        guidance_text = safe[:disclaimer_start].strip()
        disclaimer_text = safe[disclaimer_start + 5:].strip()
    else:
        guidance_text = safe
        disclaimer_text = ""

    return DrugInteractionResponse(
        medications=result.get("medications", body.medications),
        guidance=guidance_text,
        language=result["language"],
        disclaimer=disclaimer_text,
        interactions_detected=bool(raw_guidance and len(body.medications) >= 2),
    )
