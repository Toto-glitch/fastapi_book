from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from typing import TYPE_CHECKING

from .base import Base
from .associations import book_genres

if TYPE_CHECKING:
    from .book import Book


class Genre(Base):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    books: Mapped[list["Book"]] = relationship(
        "Book", secondary=book_genres, back_populates="genres"
    )
