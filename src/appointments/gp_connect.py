import logging

logger = logging.getLogger(__name__)


async def get_slots(gp_practice_id: str) -> list[dict]:
    # Stub — GP Connect FHIR R4 integration planned for Phase 3
    logger.info("GP Connect slots stub for practice %s", gp_practice_id)
    return [
        {"slot_id": "slot-001", "datetime": "2026-07-01T09:00:00", "type": "routine"},
        {"slot_id": "slot-002", "datetime": "2026-07-01T09:20:00", "type": "routine"},
        {"slot_id": "slot-003", "datetime": "2026-07-01T14:00:00", "type": "urgent"},
    ]


async def book_slot(gp_practice_id: str, slot_id: str, user_id: str, reason: str = "") -> dict:
    logger.info("GP Connect book stub: practice=%s slot=%s user=%s", gp_practice_id, slot_id, user_id)
    return {
        "booking_id": f"booking-{slot_id}",
        "status": "confirmed",
        "slot_id": slot_id,
        "gp_practice_id": gp_practice_id,
    }
