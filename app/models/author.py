from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .book import Book


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    father_name: Mapped[str | None] = mapped_column(String(255))
    birth_year: Mapped[int | None]

    books: Mapped[list["Book"]] = relationship(
        "Book", back_populates="author", cascade="all, delete-orphan"
    )
