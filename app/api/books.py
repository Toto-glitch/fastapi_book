from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from repositories import BookRepository
from schemas import BookCreate, BookResponse, BookUpdate, PaginationParams, ListResponse, DeleteResponse
from dependencies import get_book_repository, get_pagination_params

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.get("")
async def get_books(
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
    repo: Annotated[BookRepository, Depends(get_book_repository)],
) -> ListResponse[BookResponse]:
    books = await repo.get_all(offset=pagination.offset, limit=pagination.limit)
    total = await repo.count()
    return ListResponse(
        items=[BookResponse.model_validate(book) for book in books],
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@books_router.patch("/{book_id}")
async def update_book(
    book_id: int,
    new_data: BookUpdate,
    repo: Annotated[BookRepository, Depends(get_book_repository)],
) -> BookResponse:
    new_book = await repo.update(book_id, **new_data.model_dump(exclude_unset=True))
    if new_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(new_book)


@books_router.delete("/{book_id}")
async def remove_book(
    book_id: int, repo: Annotated[BookRepository, Depends(get_book_repository)]
) -> DeleteResponse:
    returning_id = await repo.remove(book_id)
    if returning_id is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return DeleteResponse(message="Book removed", id=returning_id)


@books_router.get("/{book_id}")
async def get_book_by_id(
    book_id: int, repo: Annotated[BookRepository, Depends(get_book_repository)]
) -> BookResponse:
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(book)


@books_router.post("")
async def create_book(
    book_data: BookCreate, repo: Annotated[BookRepository, Depends(get_book_repository)]
) -> BookResponse:
    book = await repo.add(**book_data.model_dump())
    return BookResponse.model_validate(book)
