from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core import get_session
from repositories import AuthorRepository, BookRepository


async def get_author_repository(
    session: AsyncSession = Depends(get_session),
) -> AuthorRepository:
    return AuthorRepository(session)


async def get_book_repository(
    session: AsyncSession = Depends(get_session),
) -> BookRepository:
    return BookRepository(session)
