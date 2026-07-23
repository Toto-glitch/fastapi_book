from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func
from typing import Generic, TypeVar, Sequence, Any

from models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, db_session: AsyncSession) -> None:
        self.session: AsyncSession = db_session

    async def add(self, **kwargs: Any) -> T:
        model_object = self.model(**kwargs)
        self.session.add(model_object)
        await self.session.flush()
        await self.session.refresh(model_object)
        return model_object

    async def all(self, offset: int = 0, limit: int = 20) -> Sequence[T]:
        query = select(self.model).offset(offset).limit(limit)
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def get(self, object_id: int) -> T | None:
        query = select(self.model).filter_by(id=object_id)
        query_result = await self.session.execute(query)
        model_object = query_result.scalar_one_or_none()
        return model_object

    async def remove(self, model_object: T) -> None:
        await self.session.delete(model_object)
        await self.session.flush()

    async def update(self, object_model: T, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(object_model, key, value)
        await self.session.flush()

    async def count(self) -> int:
        query = select(func.count()).select_from(self.model)
        query_result = await self.session.execute(query)
        return query_result.scalar_one()
