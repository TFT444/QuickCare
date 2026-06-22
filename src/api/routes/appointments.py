from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.appointments.booking import get_available_slots, book_appointment, get_user_appointments

router = APIRouter()


class BookingRequest(BaseModel):
    user_id: str
    gp_practice_id: str
    slot_id: str
    reason: Optional[str] = None
    language: Optional[str] = "en"


@router.get("/slots/{gp_practice_id}")
async def available_slots(gp_practice_id: str):
    return await get_available_slots(gp_practice_id)


@router.post("/book")
async def book(request: BookingRequest):
    result = await book_appointment(request.dict())
    if not result:
        raise HTTPException(status_code=422, detail="Booking failed")
    return result


@router.get("/user/{user_id}")
async def user_appointments(user_id: str):
    return await get_user_appointments(user_id)
