from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime


class BookBase(BaseModel):
    title: str = Field(..., max_length=255)
    price: Decimal = Field(..., decimal_places=2, max_digits=10, gt=0)
    amount: int = Field(..., ge=0)


class BookCreate(BookBase):
    author_id: int


class BookResponse(BookBase):
    id: int
    author: "AuthorResponse"
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
