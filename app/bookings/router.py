from fastapi import APIRouter, Depends

from app.bookings.DAO import BookingDAO
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_booking_by_user_id(user: Users = Depends(get_current_user)):
    return await BookingDAO.get_all(user_id=user.id)
