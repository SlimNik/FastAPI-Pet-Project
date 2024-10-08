from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import UserModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_date = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire_date})
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.JWT_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> Optional[UserModel]:
    user = await UsersDAO.get_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user