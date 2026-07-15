from sqlalchemy import select
from typing import Sequence

from .base import BaseRepository
from models import Author, Book


class AuthorRepository(BaseRepository[Author]):
    model = Author

    async def get_books(self, author_id: int, offset: int = 0, limit: int = 20) -> Sequence[Book]:
        query = select(Book).filter_by(author_id=author_id).offset(offset).limit(limit)
        query_result = await self.session.execute(query)
        return query_result.scalars().all()