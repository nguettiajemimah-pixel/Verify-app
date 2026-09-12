"""Product SQLAlchemy model for VERIFY GH."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.models.base import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    registration_number: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    manufacturer: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="Active")
    source_version: Mapped[str] = mapped_column(String(64), nullable=False, default="demo-v1")

    verifications: Mapped[list["Verification"]] = relationship(back_populates="product", cascade="all, delete-orphan")
