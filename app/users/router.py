from fastapi import APIRouter, Response

from app.exceptions import UserIsRegisteredException, InvalidLoginDataException
from app.users.DAO import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.schemas import SUserAuth


router = APIRouter(
    prefix='/auth',
    tags=['Authentification & Users'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserIsRegisteredException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise InvalidLoginDataException
    access_token = create_access_token({"sub": str(user.id)})  # рекомендация из документации
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}
