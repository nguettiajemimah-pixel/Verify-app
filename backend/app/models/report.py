"""Report SQLAlchemy model for VERIFY GH."""

from __future__ import annotations

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.models.base import TimestampMixin
from app.schemas.enums import ReportIssueType, ReportStatus


class Report(Base, TimestampMixin):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    verification_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("verifications.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    report_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    product_name: Mapped[str] = mapped_column(String(512), nullable=False)
    registration_number: Mapped[str | None] = mapped_column(String(128), nullable=True)
    manufacturer: Mapped[str | None] = mapped_column(String(512), nullable=True)
    issue_type: Mapped[ReportIssueType] = mapped_column(
        Enum(ReportIssueType, name="report_issue_type"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus, name="report_status"),
        nullable=False,
        default=ReportStatus.SUBMITTED,
    )
    internal_notes: Mapped[str] = mapped_column(Text, nullable=False, default="")

    verification: Mapped["Verification | None"] = relationship(back_populates="reports")
