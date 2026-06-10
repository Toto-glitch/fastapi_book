from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Author


class AuthorRepository:
    def __init__(self, db_session: AsyncSession):
        self.session: AsyncSession = db_session

    async def add(self, **kwargs) -> int:
        author = Author(**kwargs)
        self.session.add(author)
        await self.session.commit()
        return author.id

    async def get_by_id(self, author_id: int) -> Author | None:
        query = select(Author).filter_by(id=author_id)
        query_result = await self.session.execute(query)
        author = query_result.scalar_one_or_none()
        return author
