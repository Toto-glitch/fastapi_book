from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated

from repositories import AuthorRepository
from schemas import (
    AuthorResponse,
    AuthorCreate,
    AuthorUpdate,
    BookResponse,
    PaginationParams,
    ListResponse,
    DeleteResponse,
)
from dependencies import get_author_repository, get_pagination_params

authors_router = APIRouter(prefix="/authors", tags=["Authors"])


@authors_router.get("")
async def get_authors(
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
    repo: Annotated[AuthorRepository, Depends(get_author_repository)],
) -> ListResponse[AuthorResponse]:
    authors = await repo.all(offset=pagination.offset, limit=pagination.limit)
    total = await repo.count()
    return ListResponse(
        items=[AuthorResponse.model_validate(author) for author in authors],
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@authors_router.get("/{author_id}/books")
async def get_author_books(
    author_id: int,
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
    repo: Annotated[AuthorRepository, Depends(get_author_repository)],
) -> ListResponse[BookResponse]:
    books = await repo.get_books(
        author_id, offset=pagination.offset, limit=pagination.limit
    )
    total = await repo.count_books(author_id)
    return ListResponse(
        items=[BookResponse.model_validate(book) for book in books],
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@authors_router.delete("/{author_id}")
async def remove_author(
    author_id: int, repo: Annotated[AuthorRepository, Depends(get_author_repository)]
) -> DeleteResponse:
    author = await repo.get(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await repo.remove(author)
    return DeleteResponse(message="Author removed", id=author_id)


@authors_router.patch("/{author_id}")
async def update_author(
    author_id: int,
    new_data: AuthorUpdate,
    repo: Annotated[AuthorRepository, Depends(get_author_repository)],
) -> AuthorResponse:
    author = await repo.get(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await repo.update(author, **new_data.model_dump(exclude_unset=True))
    return AuthorResponse.model_validate(author)


@authors_router.get("/{author_id}")
async def get_author_by_id(
    author_id: int, repo: Annotated[AuthorRepository, Depends(get_author_repository)]
) -> AuthorResponse:
    author = await repo.get(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorResponse.model_validate(author)


@authors_router.post("")
async def create_author(
    author_data: AuthorCreate,
    repo: Annotated[AuthorRepository, Depends(get_author_repository)],
) -> AuthorResponse:
    author = await repo.add(**author_data.model_dump())
    return AuthorResponse.model_validate(author)
