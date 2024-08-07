from datetime import date

from fastapi import APIRouter

from app.hotels.rooms.dao import RoomsDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels & Rooms'],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel_id(hotel_id: int, date_from: date, date_to: date):
    return await RoomsDAO.get_all_by_hotel_id(hotel_id, date_from, date_to)