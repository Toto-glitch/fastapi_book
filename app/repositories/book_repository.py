from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Book


class BookRepository:
    def __init__(self, db_session: AsyncSession):
        self.session: AsyncSession = db_session

    async def add(self, **kwargs) -> int:
        book = Book(**kwargs)
        self.session.add(book)
        await self.session.commit()
        return book.id

    async def get_by_id(self, book_id: int) -> Book | None:
        query = select(Book).filter_by(id=book_id)
        query_result = await self.session.execute(query)
        book = query_result.scalar_one_or_none()
        return book
