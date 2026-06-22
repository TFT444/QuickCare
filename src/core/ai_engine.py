import os
import logging
import anthropic

from src.core.safety import append_disclaimer

logger = logging.getLogger(__name__)

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def _call(system: str, user: str, max_tokens: int = 1024) -> str:
    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text


async def explain_prescription(text: str, language: str) -> str:
    system = (
        "You are a multilingual NHS pharmacy assistant. "
        "Explain prescriptions in plain, clear language that a non-medical person can understand. "
        "Never suggest changing doses. Never make diagnoses. "
        f"Respond entirely in the language with ISO code: {language}."
    )
    user = f"Explain this prescription clearly:\n\n{text}"
    result = _call(system, user, max_tokens=1500)
    return append_disclaimer(result, language)


async def check_drug_interactions(medications: list[str], language: str) -> str:
    system = (
        "You are a multilingual NHS drug interaction checker. "
        "Report potential interactions in plain language. "
        "Never recommend dose changes. Always advise consulting a pharmacist or GP. "
        f"Respond entirely in the language with ISO code: {language}."
    )
    med_list = ", ".join(medications)
    user = f"Check for drug interactions between: {med_list}"
    result = _call(system, user, max_tokens=1000)
    return append_disclaimer(result, language)


async def triage_guidance(symptoms: str, language: str) -> str:
    system = (
        "You are a multilingual NHS triage assistant. "
        "Provide guidance on which NHS service is most appropriate (999, 111, A&E, GP, pharmacy, self-care). "
        "Never diagnose. Never prescribe. Always recommend calling 999 for life-threatening emergencies. "
        f"Respond entirely in the language with ISO code: {language}."
    )
    user = f"A patient describes these symptoms: {symptoms}"
    result = _call(system, user, max_tokens=800)
    return append_disclaimer(result, language)
