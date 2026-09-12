"""Report schemas for VERIFY GH."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.enums import ReportIssueType, ReportStatus


class ReportCreate(BaseModel):
    verification_id: Optional[int] = None
    product_name: str = Field(min_length=1, max_length=512)
    registration_number: Optional[str] = Field(default=None, max_length=128)
    manufacturer: Optional[str] = Field(default=None, max_length=512)
    issue_type: ReportIssueType
    description: str = Field(min_length=10, max_length=5000)
    location: str = Field(min_length=1, max_length=255)
    evidence_reference: Optional[str] = Field(default=None, max_length=512)


class ReportRead(BaseModel):
    id: int
    verification_id: Optional[int] = None
    report_id: str
    product_name: str
    registration_number: Optional[str] = None
    manufacturer: Optional[str] = None
    issue_type: ReportIssueType
    description: str
    location: str
    evidence_reference: Optional[str] = None
    status: ReportStatus
    internal_notes: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportStatusUpdate(BaseModel):
    status: ReportStatus
    internal_note: Optional[str] = None
