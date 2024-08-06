from datetime import date

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel_id(hotel_id: int, date_from: date, date_to: date):
    rooms_left_for_current_hotel = RoomsDAO.get_available_rooms_by_hotel_id(hotel_id, date_from, date_to)
    return rooms_left_for_current_hotel