from dependencies import (
    AuthorRepositoryDep,
    BookRepositoryDep,
    GenreRepositoryDep,
    PaginationDep,
)
from fastapi import APIRouter, HTTPException, status
from schemas import (
    BookCreate,
    BookResponse,
    BookUpdate,
    DeleteResponse,
    GenreResponse,
    ListResponse,
)

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.get("")
async def get_books(
    pagination: PaginationDep,
    repo: BookRepositoryDep,
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
    pagination: PaginationDep,
    repo: BookRepositoryDep,
) -> ListResponse[GenreResponse]:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    genres = await repo.get_genres(
        book_id, offset=pagination.offset, limit=pagination.limit
    )
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
    book_repo: BookRepositoryDep,
    genre_repo: GenreRepositoryDep,
) -> BookResponse:
    book = await book_repo.get_with_genres(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    genre = await genre_repo.get(genre_id)
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")

    await book_repo.add_genre(book, genre)
    return BookResponse.model_validate(book)


@books_router.delete("/{book_id}/genres/{genre_id}")
async def remove_genre(
    book_id: int,
    genre_id: int,
    book_repo: BookRepositoryDep,
    genre_repo: GenreRepositoryDep,
) -> BookResponse:
    book = await book_repo.get_with_genres(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    genre = await genre_repo.get(genre_id)
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")

    await book_repo.remove_genre(book, genre)
    return BookResponse.model_validate(book)


@books_router.patch("/{book_id}")
async def update_book(
    book_id: int,
    new_data: BookUpdate,
    repo: BookRepositoryDep,
) -> BookResponse:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await repo.update(book, **new_data.model_dump(exclude_unset=True))
    return BookResponse.model_validate(book)


@books_router.delete("/{book_id}")
async def remove_book(
    book_id: int, repo: BookRepositoryDep
) -> DeleteResponse:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await repo.remove(book)
    return DeleteResponse(message="Book removed", id=book_id)


@books_router.get("/{book_id}")
async def get_book_by_id(
    book_id: int, repo: BookRepositoryDep
) -> BookResponse:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BookResponse.model_validate(book)


@books_router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    book_repo: BookRepositoryDep,
    author_repo: AuthorRepositoryDep
) -> BookResponse:
    author = await author_repo.get(book_data.author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    book = await book_repo.add(**book_data.model_dump())
    return BookResponse.model_validate(book)
