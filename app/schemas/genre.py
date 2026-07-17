from pydantic import BaseModel, Field, ConfigDict


class GenreBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GenreUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    description: str | None = None
