"""Verification SQLAlchemy model for VERIFY GH."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.models.base import TimestampMixin
from app.schemas.enums import VerificationStatus


class Verification(Base, TimestampMixin):
    __tablename__ = "verifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_input: Mapped[str] = mapped_column(String(2000), nullable=False)
    product_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    match_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus, name="verification_status"),
        nullable=False,
    )
    matched_fields: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    mismatched_fields: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    unavailable_fields: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    registry_version: Mapped[str] = mapped_column(String(64), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    product: Mapped["Product | None"] = relationship(back_populates="verifications")
    reports: Mapped[list["Report"]] = relationship(back_populates="verification", cascade="all, delete-orphan")
