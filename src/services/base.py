from sqlalchemy import delete, update
from sqlalchemy.future import select

from src.database.db import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, limit: int = None, offset: int = None, **filter_by):
        query = select(cls.model).filter_by(**filter_by)

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        async with async_session() as session:
            result = await session.execute(query)

        return result.scalars().all()

    @classmethod
    async def find_one_by_filters(cls, **filter_by):
        query = select(cls.model).filter_by(**filter_by)

        async with async_session() as session:
            result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    async def add_one(cls, entity):
        async with async_session() as session:
            session.add(entity)
            await session.commit()

    @classmethod
    async def update_one(cls, entity_id: int, **update_data):
        async with async_session() as session:
            query = (
                update(cls.model).where(cls.model.id == entity_id).values(**update_data)
            )
            await session.execute(query)
            await session.commit()

            result = await session.execute(
                select(cls.model).where(cls.model.id == entity_id)
            )
            return result.scalar_one()

    @classmethod
    async def delete_one(cls, **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        async with async_session() as session:
            await session.execute(query)
            await session.commit()
