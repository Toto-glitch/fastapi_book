from sqlalchemy import select, func
from typing import Sequence

from .base import BaseRepository
from models import Book, Genre


class BookRepository(BaseRepository[Book]):
    model = Book

    async def get_genres(self, book_id: int, offset: int = 0, limit: int = 20) -> Sequence[Genre]:
        query = (
            select(Genre)
            .join(Genre.books)
            .filter(Book.id == book_id)
            .offset(offset)
            .limit(limit)
        )
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def count_genres(self, book_id: int) -> int:
        query = (
            select(func.count(Genre.id))
            .join(Genre.books)
            .filter(Book.id == book_id)
        )
        query_result = await self.session.execute(query)
        return query_result.scalar_one()
