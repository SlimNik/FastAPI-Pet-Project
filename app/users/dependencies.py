from datetime import datetime

from fastapi import Depends, Request, HTTPException, status
from jose import jwt, JWTError

from app.config import settings
from app.users.DAO import UsersDAO
from app.users.models import Users


def get_token(request: Request) -> str:
    token = request.cookies.get('booking_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


# Depends используется, т.к. запрос сущетствует только в пределе одного ендпойнта
# если запрос исползьуется в другой функции, то будет что-то там до самого ендпойта
# FastAPI вызывает фунцию, указанную в Depends, создавая своеобразную цепочку вызовов
async def get_current_user(token: str = Depends(get_token)) -> Users:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_KEY,
            settings.JWT_ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT decode error')
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No user id')
    user = await UsersDAO.get_by_id(model_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user id')
    return user
