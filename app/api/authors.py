from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException, Query

from repositories import AuthorRepository
from schemas import AuthorResponse, AuthorCreate
from core import get_session


async def get_author_repository(session: AsyncSession = Depends(get_session)) -> AuthorRepository:
    return AuthorRepository(session)


authors_router = APIRouter(prefix="/authors", tags=["Authors"])


@authors_router.get("")
async def get_authors(
    page: int = Query(1),
    limit: int = Query(20),
    repo: AuthorRepository = Depends(get_author_repository)
):
    authors = await repo.get_all(offset=page - 1, limit=limit)
    result = [AuthorResponse.model_validate(author) for author in authors]
    return result


@authors_router.delete("/{author_id}")
async def remove_author(
        author_id: int,
        repo: AuthorRepository = Depends(get_author_repository)
):
    await repo.remove(author_id)
    return {"message": "Author removed", "author_id": author_id}


@authors_router.get("/{author_id}")
async def get_author_by_id(author_id: int, repo: AuthorRepository = Depends(get_author_repository)):
    author = await repo.get_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorResponse.model_validate(author)


@authors_router.post("")
async def create_author(author_data: AuthorCreate, repo: AuthorRepository = Depends(get_author_repository)):
    author_id = await repo.add(**author_data.model_dump())
    return {"message": "Author created", "author_id": author_id}
