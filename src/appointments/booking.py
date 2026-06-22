from src.appointments.gp_connect import get_slots, book_slot


async def get_available_slots(gp_practice_id: str) -> dict:
    slots = await get_slots(gp_practice_id)
    return {"gp_practice_id": gp_practice_id, "slots": slots}


async def book_appointment(data: dict) -> dict | None:
    result = await book_slot(
        gp_practice_id=data["gp_practice_id"],
        slot_id=data["slot_id"],
        user_id=data["user_id"],
        reason=data.get("reason", ""),
    )
    return result


async def get_user_appointments(user_id: str) -> list[dict]:
    # Stub — integrate with NHS FHIR patient record in Phase 3
    return []
