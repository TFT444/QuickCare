_CONTEXT: dict[str, dict] = {
    "ur": {
        "greeting_style": "formal",
        "family_involvement": True,
        "mental_health_sensitivity": "high",
        "notes": "Urdu-speaking patients may prefer family members to be present during consultations.",
    },
    "bn": {
        "greeting_style": "respectful",
        "family_involvement": True,
        "mental_health_sensitivity": "high",
        "notes": "Mental health discussions may carry stigma — use indirect, supportive language.",
    },
    "so": {
        "greeting_style": "warm",
        "family_involvement": True,
        "mental_health_sensitivity": "very_high",
        "notes": "Community and religious context is important. Clan and family are central to wellbeing.",
    },
    "ar": {
        "greeting_style": "formal",
        "family_involvement": True,
        "mental_health_sensitivity": "high",
        "notes": "Religious context (halal medication, prayer times) may affect care preferences.",
    },
    "en": {
        "greeting_style": "friendly",
        "family_involvement": False,
        "mental_health_sensitivity": "moderate",
        "notes": "",
    },
}


def get_context(language: str) -> dict:
    return _CONTEXT.get(language, _CONTEXT["en"])
