from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query

from app.hotels.rooms.dao import RoomsDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels & Rooms'],
)


@router.get('')
async def get_all_rooms():
    return await RoomsDAO.get_all()


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel_id(
        hotel_id: int,
        date_from: date = Query(..., description=f'Например {datetime.now().date()}'),
        date_to: date = Query(..., description=f'Например {datetime.now().date() + timedelta(days=7)}')
):
    return await RoomsDAO.get_all_by_hotel_id(hotel_id, date_from, date_to)