from dependencies import AuthorOr404Dep, AuthorRepositoryDep, PaginationDep
from fastapi import APIRouter, status
from schemas import (
    AuthorCreate,
    AuthorResponse,
    AuthorUpdate,
    BookResponse,
    DeleteResponse,
    ListResponse,
)

authors_router = APIRouter(prefix="/authors", tags=["Authors"])


@authors_router.get("")
async def get_authors(
    pagination: PaginationDep,
    repo: AuthorRepositoryDep,
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
    author: AuthorOr404Dep,
    pagination: PaginationDep,
    repo: AuthorRepositoryDep,
) -> ListResponse[BookResponse]:
    books = await repo.get_books(
        author.id, offset=pagination.offset, limit=pagination.limit
    )
    total = await repo.count_books(author.id)
    return ListResponse(
        items=[BookResponse.model_validate(book) for book in books],
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@authors_router.delete("/{author_id}")
async def remove_author(
    author: AuthorOr404Dep, repo: AuthorRepositoryDep
) -> DeleteResponse:
    await repo.remove(author)
    return DeleteResponse(message="Author removed", id=author.id)


@authors_router.patch("/{author_id}")
async def update_author(
    author: AuthorOr404Dep,
    new_data: AuthorUpdate,
    repo: AuthorRepositoryDep,
) -> AuthorResponse:
    await repo.update(author, **new_data.model_dump(exclude_unset=True))
    return AuthorResponse.model_validate(author)


@authors_router.get("/{author_id}")
async def get_author_by_id(
    author: AuthorOr404Dep, repo: AuthorRepositoryDep
) -> AuthorResponse:
    return AuthorResponse.model_validate(author)

    
@authors_router.post("", status_code=status.HTTP_201_CREATED)
async def create_author(
    author_data: AuthorCreate,
    repo: AuthorRepositoryDep,
) -> AuthorResponse:
    author = await repo.add(**author_data.model_dump())
    return AuthorResponse.model_validate(author)
