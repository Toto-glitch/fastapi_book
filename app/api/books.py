from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_session
from repositories import BookRepository
from schemas import BookCreate, BookResponse


async def get_book_repository(session: AsyncSession = Depends(get_session)) -> BookRepository:
    return BookRepository(session)


books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.get("")
async def get_books(
        page: int = Query(1),
        limit: int = Query(20),
        repo: BookRepository = Depends(get_book_repository)
):
    books = await repo.get_all(offset=page - 1, limit=limit)
    result = [BookResponse.model_validate(book) for book in books]
    return result


@books_router.delete("/{book_id}")
async def remove_book(
        book_id: int,
        repo: BookRepository = Depends(get_book_repository)
):
    await repo.remove(book_id)
    return {"message": "Book removed", "book_id": book_id}


@books_router.get("/{book_id}")
async def get_book_by_id(book_id: int, repo: BookRepository = Depends(get_book_repository)):
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(book)


@books_router.post("")
async def create_book(book_data: BookCreate, repo: BookRepository = Depends(get_book_repository)):
    book_id = await repo.add(**book_data.model_dump())
    return {"message": "Book created", "book_id": book_id}
