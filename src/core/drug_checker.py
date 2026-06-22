from src.core.ai_engine import check_drug_interactions


async def check(medications: list[str], language: str = "en") -> dict:
    if len(medications) < 2:
        return {"interactions": [], "guidance": "", "language": language}

    guidance = await check_drug_interactions(medications, language)
    return {
        "medications": medications,
        "language": language,
        "guidance": guidance,
        "interactions": [],  # placeholder for future BNF data integration
    }
