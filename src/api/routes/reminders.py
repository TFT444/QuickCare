from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.reminders.scheduler import create_reminder, get_reminder, delete_reminder, list_reminders

router = APIRouter()


class ReminderCreate(BaseModel):
    user_id: str
    medication: str
    dose: str
    times: list[str]  # HH:MM strings
    start_date: str   # ISO date


class ReminderResponse(BaseModel):
    id: str
    user_id: str
    medication: str
    dose: str
    times: list[str]
    start_date: str
    active: bool


@router.post("/", response_model=ReminderResponse)
async def create(reminder: ReminderCreate):
    return await create_reminder(reminder.dict())


@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get(reminder_id: str):
    result = await get_reminder(reminder_id)
    if not result:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return result


@router.get("/user/{user_id}")
async def list_user_reminders(user_id: str):
    return await list_reminders(user_id)


@router.delete("/{reminder_id}")
async def delete(reminder_id: str):
    deleted = await delete_reminder(reminder_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"deleted": True}
