from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BaseRepository:
    model = None

    def __init__(self, db_session: AsyncSession):
        self.session: AsyncSession = db_session

    async def add(self, **kwargs) -> int:
        model_object = self.model(**kwargs)
        self.session.add(model_object)
        await self.session.commit()
        return model_object.id

    async def get_all(self, offset: int = 0, limit: int = 20):
        query = select(self.model).offset(offset).limit(limit)
        query_result = await self.session.execute(query)
        return query_result.scalars().all()

    async def get_by_id(self, object_id: int):
        query = select(self.model).filter_by(id=object_id)
        query_result = await self.session.execute(query)
        model_object = query_result.scalar_one_or_none()
        return model_object

