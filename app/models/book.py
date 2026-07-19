from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, func, Numeric
from decimal import Decimal
from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base
from .associations import book_genres

if TYPE_CHECKING:
    from .author import Author
    from .genre import Genre


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(255))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    author: Mapped["Author"] = relationship(
        "Author", back_populates="books", lazy="joined"
    )
    genres: Mapped[list["Genre"]] = relationship("Genre", secondary=book_genres, back_populates="books")
