from fastapi import APIRouter

from app.bookings.DAO import BookingDAO


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_booking_by_id():
    return await BookingDAO.get_by_id(1)
