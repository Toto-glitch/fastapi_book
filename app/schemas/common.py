from pydantic import BaseModel, Field
from typing import Generic, TypeVar

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class ListResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int


class DeleteResponse(BaseModel):
    message: str
    id: int
