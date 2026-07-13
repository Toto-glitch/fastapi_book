from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
