from dependencies import GenreRepositoryDep, PaginationDep
from fastapi import APIRouter, HTTPException, status
from schemas import (
    DeleteResponse,
    GenreCreate,
    GenreResponse,
    GenreUpdate,
    ListResponse,
)

genres_router = APIRouter(prefix="/genres", tags=["Genres"])


@genres_router.get("")
async def get_genres(
    pagination: PaginationDep,
    repo: GenreRepositoryDep,
) -> ListResponse[GenreResponse]:
    genres = await repo.all(offset=pagination.offset, limit=pagination.limit)
    total = await repo.count()
    return ListResponse(
        items=[GenreResponse.model_validate(genre) for genre in genres],
        total=total,
        page=pagination.page,
        limit=pagination.limit,
    )


@genres_router.post("", status_code=status.HTTP_201_CREATED)
async def create_genre(
    genre_data: GenreCreate,
    repo: GenreRepositoryDep,
) -> GenreResponse:
    genre = await repo.add(**genre_data.model_dump())
    return GenreResponse.model_validate(genre)


@genres_router.get("/{genre_id}")
async def get_genre_by_id(
    genre_id: int, repo: GenreRepositoryDep
) -> GenreResponse:
    genre = await repo.get(genre_id)
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    return GenreResponse.model_validate(genre)


@genres_router.patch("/{genre_id}")
async def update_genre(
    genre_id: int,
    new_data: GenreUpdate,
    repo: GenreRepositoryDep,
) -> GenreResponse:
    genre = await repo.get(genre_id)
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    await repo.update(genre, **new_data.model_dump(exclude_unset=True))
    return GenreResponse.model_validate(genre)


@genres_router.delete("/{genre_id}")
async def remove_genre(
    genre_id: int, repo: GenreRepositoryDep
) -> DeleteResponse:
    genre = await repo.get(genre_id)
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")
    await repo.remove(genre)
    return DeleteResponse(message="Genre removed", id=genre_id)
