import uuid
import hashlib
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    original_text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    language = Column(String(10), default="en")
    medications = Column(JSON, default=list)
    audit_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def compute_hash(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()
