from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from dependencies import get_pagination_params, get_genre_repository
from schemas import PaginationParams, ListResponse, GenreResponse, GenreCreate, GenreUpdate
from repositories import GenreRepository

genres_router = APIRouter(prefix="/genres", tags=["Genres"])


@genres_router.get("")
async def get_genres(
        pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
        repo: Annotated[GenreRepository, Depends(get_genre_repository)]
) -> ListResponse[GenreResponse]:
    genres = await repo.get_all(offset=pagination.offset, limit=pagination.limit)
    total = await repo.count()
    return ListResponse(
        items=[GenreResponse.model_validate(genre) for genre in genres],
        total=total.imag,
        page=pagination.page,
        limit=pagination.limit,
    )
