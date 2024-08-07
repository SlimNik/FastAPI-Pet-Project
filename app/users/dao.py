from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session
from app.users.models import UserModel


class UsersDAO(BaseDAO):
    model = UserModel

    @classmethod  # использум метод класса, чтобы каждый раз не создавать новый объект
    async def get_all(cls):
        async with async_session() as session:
            query = select(UserModel.id.label('user_id'), UserModel.email)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_by_id(cls, user_id: int):
        async with async_session() as session:
            query = select(UserModel.id.label('user_id'), UserModel.email).filter_by(id=user_id)
        result = await session.execute(query)
        return result.mappings().one()