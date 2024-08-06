from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.DAO import BookingDAO
from app.exceptions import RoomCannotBeBookedException
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_booking_by_user_id(current_user: Users = Depends(get_current_user)):
    return await BookingDAO.get_all(user_id=current_user.id)


@router.post('')
async def get_bookings(
        room_id: int,
        date_from: date,
        date_to: date,
        current_user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(current_user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException