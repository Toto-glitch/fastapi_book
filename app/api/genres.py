from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from dependencies import get_pagination_params, get_genre_repository
from schemas import PaginationParams, ListResponse, GenreResponse, GenreCreate, GenreUpdate, DeleteResponse
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
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@genres_router.post("")
async def create_genre(
        genre_data: GenreCreate,
        repo: Annotated[GenreRepository, Depends(get_genre_repository)]
) -> GenreResponse:
    genre = await repo.add(**genre_data.model_dump())
    return GenreResponse.model_validate(genre)


@genres_router.get("/{genre_id}")
async def get_genre_by_id(
        genre_id: int,
        repo: Annotated[GenreRepository, Depends(get_genre_repository)]
) -> GenreResponse:
    genre = await repo.get_by_id(genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return GenreResponse.model_validate(genre)


@genres_router.patch("/{genre_id}")
async def update_genre(
        genre_id: int,
        new_data: GenreUpdate,
        repo: Annotated[GenreRepository, Depends(get_genre_repository)]
) -> GenreResponse:
    new_genre = await repo.update(genre_id, **new_data.model_dump(exclude_unset=True))
    if new_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return GenreResponse.model_validate(new_genre)


@genres_router.delete("/{genre_id}")
async def remove_genre(
        genre_id: int,
        repo: Annotated[GenreRepository, Depends(get_genre_repository)]
) -> DeleteResponse:
    returning_id = await repo.remove(genre_id)
    if returning_id is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return DeleteResponse(message="Genre removed", id=returning_id)
