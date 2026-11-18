from collections.abc import Sequence

from models import Book, Genre
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from .base import BaseRepository


class BookRepository(BaseRepository[Book]):
    model = Book

    async def get_with_genres(self, book_id: int) -> Book | None:
        query = select(Book).filter_by(id=book_id).options(selectinload(Book.genres))
        query_result = await self.session.execute(query)
        return query_result.scalar_one_or_none()

    async def add_genre(self, book: Book, genre: Genre) -> None:
        if genre not in book.genres:
            book.genres.append(genre)
        await self.session.flush()

    async def remove_genre(self, book: Book, genre: Genre) -> None:
        if genre in book.genres:
            book.genres.remove(genre)
        await self.session.flush()

    async def get_genres(
        self, book_id: int, offset: int = 0, limit: int = 20
    ) -> Sequence[Genre]:
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
            select(func.count(Genre.id)).join(Genre.books).filter(Book.id == book_id)
        )
        query_result = await self.session.execute(query)
        return query_result.scalar_one()
