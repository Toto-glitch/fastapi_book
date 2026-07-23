from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from repositories import BookRepository, GenreRepository
from schemas import (
    BookCreate,
    BookResponse,
    BookUpdate,
    PaginationParams,
    ListResponse,
    DeleteResponse,
    GenreResponse
)
from dependencies import get_book_repository, get_pagination_params, get_genre_repository

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.get("")
async def get_books(
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
    repo: Annotated[BookRepository, Depends(get_book_repository)],
) -> ListResponse[BookResponse]:
    books = await repo.all(offset=pagination.offset, limit=pagination.limit)
    total = await repo.count()
    return ListResponse(
        items=[BookResponse.model_validate(book) for book in books],
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@books_router.get("/{book_id}/genres")
async def get_book_genres(
        book_id: int,
        pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
        repo: Annotated[BookRepository, Depends(get_book_repository)]
) -> ListResponse[GenreResponse]:
    genres = await repo.get_genres(book_id, offset=pagination.offset, limit=pagination.limit)
    total = await repo.count_genres(book_id)
    return ListResponse(
        items=[GenreResponse.model_validate(genre) for genre in genres],
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@books_router.post("/{book_id}/genres/{genre_id}")
async def add_genre(
        book_id: int,
        genre_id: int,
        book_repo: Annotated[BookRepository, Depends(get_book_repository)],
        genre_repo: Annotated[GenreRepository, Depends(get_genre_repository)],
) -> BookResponse:
    book = await book_repo.get_with_genres(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    genre = await genre_repo.get(genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    await book_repo.add_genre(book, genre)
    return BookResponse.model_validate(book)


@books_router.patch("/{book_id}")
async def update_book(
    book_id: int,
    new_data: BookUpdate,
    repo: Annotated[BookRepository, Depends(get_book_repository)],
) -> BookResponse:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await repo.update(book, **new_data.model_dump(exclude_unset=True))
    return BookResponse.model_validate(book)


@books_router.delete("/{book_id}")
async def remove_book(
    book_id: int, repo: Annotated[BookRepository, Depends(get_book_repository)]
) -> DeleteResponse:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await repo.remove(book)
    return DeleteResponse(message="Book removed", id=book_id)


@books_router.get("/{book_id}")
async def get_book_by_id(
    book_id: int, repo: Annotated[BookRepository, Depends(get_book_repository)]
) -> BookResponse:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(book)


@books_router.post("")
async def create_book(
    book_data: BookCreate, repo: Annotated[BookRepository, Depends(get_book_repository)]
) -> BookResponse:
    book = await repo.add(**book_data.model_dump())
    return BookResponse.model_validate(book)
