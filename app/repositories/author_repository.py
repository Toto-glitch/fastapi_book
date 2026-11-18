from collections.abc import Sequence

from models import Author, Book
from sqlalchemy import func, select

from .base import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    model = Author

    async def get_books(
        self, author_id: int, offset: int = 0, limit: int = 20
    ) -> Sequence[Book]:
        query = (
            select(Book)
            .join(Book.author)
            .filter(Author.id == author_id)
            .offset(offset)
            .limit(limit)
        )
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def count_books(self, author_id: int) -> int:
        query = (
            select(func.count(Book.id)).join(Book.author).filter(Author.id == author_id)
        )
        query_result = await self.session.execute(query)
        return query_result.scalar_one()
