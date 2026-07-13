from fastapi import Depends, APIRouter, HTTPException

from repositories import AuthorRepository
from schemas import AuthorResponse, AuthorCreate, AuthorUpdate, BookResponse, PaginationParams
from dependencies import get_author_repository, get_pagination_params

authors_router = APIRouter(prefix="/authors", tags=["Authors"])


@authors_router.get("")
async def get_authors(
    pagination: PaginationParams = Depends(get_pagination_params),
    repo: AuthorRepository = Depends(get_author_repository),
):
    authors = await repo.get_all(offset=pagination.offset, limit=pagination.limit)
    result = [AuthorResponse.model_validate(author) for author in authors]
    return result


@authors_router.get("/{author_id}/books")
async def get_author_books(
        author_id: int,
        pagination: PaginationParams = Depends(get_pagination_params),
        repo: AuthorRepository = Depends(get_author_repository)
):
    books = await repo.get_books(author_id, offset=pagination.offset, limit=pagination.limit)
    result = [BookResponse.model_validate(book) for book in books]
    return result


@authors_router.delete("/{author_id}")
async def remove_author(
    author_id: int, repo: AuthorRepository = Depends(get_author_repository)
):
    returning_id = await repo.remove(author_id)
    if returning_id is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"message": "Author removed", "author_id": author_id}


@authors_router.patch("/{author_id}")
async def update_author(
    author_id: int,
    new_data: AuthorUpdate,
    repo: AuthorRepository = Depends(get_author_repository),
):
    new_author = await repo.update(author_id, **new_data.model_dump(exclude_unset=True))
    if new_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return {
        "message": "Author updated",
        "new_author": AuthorResponse.model_validate(new_author),
    }


@authors_router.get("/{author_id}")
async def get_author_by_id(
    author_id: int, repo: AuthorRepository = Depends(get_author_repository)
):
    author = await repo.get_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorResponse.model_validate(author)


@authors_router.post("")
async def create_author(
    author_data: AuthorCreate, repo: AuthorRepository = Depends(get_author_repository)
):
    author_id = await repo.add(**author_data.model_dump())
    return {"message": "Author created", "author_id": author_id}
