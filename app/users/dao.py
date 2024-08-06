from app.dao.base import BaseDAO
from app.users.models import UserModel


class UsersDAO(BaseDAO):
    model = UserModel