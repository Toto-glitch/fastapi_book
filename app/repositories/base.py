from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, Sequence
from typing import Generic, TypeVar

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, db_session: AsyncSession):
        self.session: AsyncSession = db_session

    async def add(self, **kwargs) -> int:
        model_object = self.model(**kwargs)
        self.session.add(model_object)
        await self.session.flush()
        return model_object.id

    async def get_all(self, offset: int = 0, limit: int = 20) -> Sequence[ModelType]:
        query = select(self.model).offset(offset).limit(limit)
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def get_by_id(self, object_id: int) -> ModelType | None:
        query = select(self.model).filter_by(id=object_id)
        query_result = await self.session.execute(query)
        model_object = query_result.scalar_one_or_none()
        return model_object

    async def remove(self, object_id: int) -> int | None:
        query = delete(self.model).filter_by(id=object_id).returning(self.model.id)
        query_result = await self.session.execute(query)
        await self.session.flush()
        return query_result.scalar_one_or_none()

    async def update(self, object_id: int, **kwargs) -> ModelType | None:
        model_object = await self.get_by_id(object_id)
        if model_object is None:
            return None
        for key, value in kwargs.items():
            setattr(model_object, key, value)
        await self.session.flush()
        await self.session.refresh(model_object)
        return model_object
