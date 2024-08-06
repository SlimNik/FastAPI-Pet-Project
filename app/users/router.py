from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, InvalidLoginDataException
from app.users.DAO import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import Users
from app.users.schemas import SUserAuth


router = APIRouter(
    prefix='/auth',
    tags=['Authentification & Users'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth) -> None:
    existing_user = await UsersDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth) -> dict:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise InvalidLoginDataException
    access_token = create_access_token({"sub": str(user.id)})  # рекомендация из документации
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post('/logout')
async def logout_user(response: Response) -> None:
    response.delete_cookie("booking_access_token", httponly=True)


@router.get('/me')
async def read_me_user_data(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get('/all')
async def read_all_user_data(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.get_all()