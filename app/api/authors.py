from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException

from repositories import AuthorRepository
from schemas import AuthorResponse, AuthorCreate
from core import get_session


async def get_author_repository(session: AsyncSession = Depends(get_session)) -> AuthorRepository:
    return AuthorRepository(session)


authors_router = APIRouter(prefix="/authors", tags=["Authors"])


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
