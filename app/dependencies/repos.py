from typing import Annotated

from core import get_session
from fastapi import Depends, HTTPException, status
from models import Author, Book, Genre
from repositories import AuthorRepository, BookRepository, GenreRepository
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_author_repository(
    session: SessionDep,
) -> AuthorRepository:
    return AuthorRepository(session)


async def get_book_repository(
    session: SessionDep,
) -> BookRepository:
    return BookRepository(session)


async def get_genre_repository(
    session: SessionDep,
) -> GenreRepository:
    return GenreRepository(session)


AuthorRepositoryDep = Annotated[AuthorRepository, Depends(get_author_repository)]
BookRepositoryDep = Annotated[BookRepository, Depends(get_book_repository)]
GenreRepositoryDep = Annotated[GenreRepository, Depends(get_genre_repository)]


async def get_author_or_404(author_id: int, repo: AuthorRepositoryDep) -> Author:
    author = await repo.get(author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The author is not found")
    return author


async def get_book_or_404(book_id: int, repo: BookRepositoryDep) -> Book:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The book is not found")
    return book


async def get_genre_or_404(genre_id: int, repo: GenreRepositoryDep) -> Genre:
    genre = await repo.get(genre_id)
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The genre is not found")
    return genre


AuthorOr404Dep = Annotated[Author, Depends(get_author_or_404)]
BookOr404Dep = Annotated[Book, Depends(get_book_or_404)]
GenreOr404Dep = Annotated[Genre, Depends(get_genre_or_404)]
