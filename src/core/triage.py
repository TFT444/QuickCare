from src.core.ai_engine import triage_guidance


async def assess(symptoms: str, language: str = "en") -> dict:
    guidance = await triage_guidance(symptoms, language)
    return {
        "symptoms": symptoms,
        "language": language,
        "guidance": guidance,
    }
