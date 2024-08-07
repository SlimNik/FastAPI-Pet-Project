from sqlalchemy import select, insert, delete

from app.database import async_session


# базовый класс для общих запросов
class BaseDAO:
    model = None

    @classmethod  # использум метод класса, чтобы каждый раз не создавать новый объект
    async def get_all(cls, **filter_kwargs):
        async with async_session() as session:
            query = select(cls.model.__table__).filter_by(**filter_kwargs)
            # result.all() возвращает список кортежей с моделями
            # result.scalars().all() возвращает список моделей
            result = await session.execute(query)
            # return result.mappings().all()
            return result.mappings().all()

    @classmethod
    async def get_one_or_none(cls, **filter_kwargs):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_kwargs):
        async with async_session() as session:
            query = delete(cls.model).filter_by(**filter_kwargs)
            await session.execute(query)
            await session.commit()