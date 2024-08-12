from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.bookings.dao import BookingsDAO
from app.bookings.schemas import BookingSchema
from app.exceptions import RoomCannotBeBookedException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import UserModel


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings(current_user: UserModel = Depends(get_current_user)):
    return await BookingsDAO.get_all(user_id=int(current_user.id))


@router.post('/add')
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        current_user: UserModel = Depends(get_current_user),
) -> None:
    booking = await BookingsDAO.add(current_user.id, room_id, date_from, date_to)

    booking_adapter = TypeAdapter(BookingSchema)
    booking_dict = booking_adapter.validate_python(booking).dict()
    send_booking_confirmation_email.delay(booking_dict)

    if not booking:
        raise RoomCannotBeBookedException


@router.delete('/{booking_id}')
async def delete_booking(booking_id: int, current_user: UserModel = Depends(get_current_user)) -> None:
    await BookingsDAO.delete(id=booking_id)