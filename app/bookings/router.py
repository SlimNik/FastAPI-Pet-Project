from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingsDAO
from app.exceptions import RoomCannotBeBookedException
from app.users.dependencies import get_current_user
from app.users.models import UserModel


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_booking_by_user_id(current_user: UserModel = Depends(get_current_user)):
    return await BookingsDAO.get_all(user_id=int(current_user.id))


@router.post('/create')
async def create_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        current_user: UserModel = Depends(get_current_user),
) -> None:
    booking = await BookingsDAO.add(current_user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException


@router.delete('/{booking_id}')
async def delete_booking(booking_id: int) -> None:
    await BookingsDAO.delete(id=booking_id)