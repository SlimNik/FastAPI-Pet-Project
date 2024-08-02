from fastapi import APIRouter


router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
def get_booking():
    pass


@router.get('/{booking_id}')
def get_certain_booking(booking_id):
    return booking_id
