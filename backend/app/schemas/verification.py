"""Verification schemas for VERIFY GH."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.enums import VerificationStatus


class VerificationCreate(BaseModel):
    registration_number: str = Field(min_length=1, max_length=128)
    product_name: Optional[str] = Field(default=None, max_length=512)
    manufacturer: Optional[str] = Field(default=None, max_length=512)


class VerificationRead(BaseModel):
    id: int
    user_input: str
    product_id: Optional[int] = None
    match_status: VerificationStatus
    matched_fields: str
    mismatched_fields: str
    unavailable_fields: str
    registry_version: str
    explanation: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VerificationResult(BaseModel):
    status: VerificationStatus
    product_id: Optional[int] = None
    registry_version: str
    matched_fields: list[str]
    mismatched_fields: list[str]
    unavailable_fields: list[str]
    explanation: str
