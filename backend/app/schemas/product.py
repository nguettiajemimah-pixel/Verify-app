"""Product schemas for VERIFY GH."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=512)
    category: str = Field(min_length=1, max_length=128)
    registration_number: str = Field(min_length=1, max_length=128)
    manufacturer: str = Field(min_length=1, max_length=512)


class ProductCreate(ProductBase):
    status: str = "Active"
    source_version: str = "demo-v1"


class ProductRead(ProductBase):
    id: int
    status: str
    source_version: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductSearch(BaseModel):
    query: str = Field(min_length=1, max_length=512)
    category: Optional[str] = None
