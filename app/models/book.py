from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, func
from decimal import Decimal
from datetime import datetime

from core import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    price: Mapped[Decimal]
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    author: Mapped['Author'] = relationship("Author", back_populates="books")
