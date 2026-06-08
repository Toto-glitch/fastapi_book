from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

from core import Base
from .associations import book_genres_table


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)

    books: Mapped[list['Book']] = relationship(secondary=book_genres_table, back_populates="genres")
