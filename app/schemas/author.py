from pydantic import BaseModel, Field, ConfigDict


class AuthorBase(BaseModel):
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    father_name: str | None = Field(None, max_length=255)
    birth_year: int | None = Field(None, ge=1, le=9999)


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    first_name: str | None = Field(None, max_length=255)
    last_name: str | None = Field(None, max_length=255)
    father_name: str | None = Field(None, max_length=255)
    birth_year: int | None = Field(None, ge=1, le=9999)
