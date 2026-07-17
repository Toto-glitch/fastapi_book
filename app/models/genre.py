from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text

from .base import Base


class Genre(Base):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
