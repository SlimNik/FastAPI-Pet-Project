from datetime import datetime

from fastapi import Depends, Request
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import AbsentTokenException, UserIsNotPresentException, ExpiredToeknException, InvalidTokenFormatException
from app.users.DAO import UsersDAO
from app.users.models import Users


def get_token(request: Request) -> str:
    token = request.cookies.get('booking_access_token')
    if not token:
        raise AbsentTokenException
    return token


# Использование Depends оправдано, поскольку запрос существует только в контексте одного эндпоинта.
# Если бы запрос использовался в другой функции, это могло бы привести к сложной цепочке вызовов до самого эндпоинта.
# FastAPI вызывает функцию, указанную в Depends, создавая цепочку вызовов, что упрощает управление зависимостями.
async def get_current_user(token: str = Depends(get_token)) -> Users:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_KEY,
            settings.JWT_ALGORITHM
        )
    except JWTError:
        raise InvalidTokenFormatException
    expire: str = payload.get('exp')
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise ExpiredToeknException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.get_by_id(model_id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
