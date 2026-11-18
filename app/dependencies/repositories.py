from typing import Annotated

from core import get_session
from fastapi import Depends
from repositories import AuthorRepository, BookRepository, GenreRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def get_author_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthorRepository:
    return AuthorRepository(session)


async def get_book_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> BookRepository:
    return BookRepository(session)


async def get_genre_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> GenreRepository:
    return GenreRepository(session)
