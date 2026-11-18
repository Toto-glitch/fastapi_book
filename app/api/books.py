from dependencies import (
    AuthorOr404Dep,
    BookOr404Dep,
    BookRepositoryDep,
    GenreOr404Dep,
    PaginationDep,
)
from fastapi import APIRouter, status
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
    book: BookOr404Dep,
    pagination: PaginationDep,
    repo: BookRepositoryDep,
) -> ListResponse[GenreResponse]:
    genres = await repo.get_genres(
        book.id, offset=pagination.offset, limit=pagination.limit
    )
    total = await repo.count_genres(book.id)
    return ListResponse(
        items=[GenreResponse.model_validate(genre) for genre in genres],
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@books_router.post("/{book_id}/genres/{genre_id}")
async def add_genre(
    book: BookOr404Dep,
    genre: GenreOr404Dep,
    repo: BookRepositoryDep
) -> BookResponse:
    await repo.add_genre(book, genre)
    return BookResponse.model_validate(book)


@books_router.delete("/{book_id}/genres/{genre_id}")
async def remove_genre(
    book: BookOr404Dep,
    genre: GenreOr404Dep,
    book_repo: BookRepositoryDep
) -> BookResponse:
    await book_repo.remove_genre(book, genre)
    return BookResponse.model_validate(book)


@books_router.patch("/{book_id}")
async def update_book(
    book: BookOr404Dep,
    new_data: BookUpdate,
    repo: BookRepositoryDep,
) -> BookResponse:
    await repo.update(book, **new_data.model_dump(exclude_unset=True))
    return BookResponse.model_validate(book)


@books_router.delete("/{book_id}")
async def remove_book(
    book: BookOr404Dep, repo: BookRepositoryDep
) -> DeleteResponse:
    await repo.remove(book)
    return DeleteResponse(message="Book removed", id=book.id)


@books_router.get("/{book_id}")
async def get_book_by_id(
    book: BookOr404Dep, repo: BookRepositoryDep
) -> BookResponse:
    return BookResponse.model_validate(book)


@books_router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(
    author: AuthorOr404Dep,
    book_data: BookCreate,
    repo: BookRepositoryDep,
) -> BookResponse:
    book = await repo.add(**book_data.model_dump())
    return BookResponse.model_validate(book)
