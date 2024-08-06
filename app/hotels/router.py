from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import HotelSchema


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels & Rooms'],
)


# class HotelSearchArgs:
#     def __init__(self,
#                  hotel_id: int,
#                  hotel_name: str,
#                  date_from: date,
#                  date_to: date,
#                  stars: Optional[int] = Query(None, gt=0, lt=6),
#                  sea_view: Optional[bool] = None
#                  ):
#         self.hotel_id = hotel_id
#         self.hotel_name = hotel_name
#         self.date_from = date_from
#         self.date_to = date_to
#         self.stars = stars
#         self.sea_view = sea_view

@router.get('/id/{hotel_id}')
async def get_hotel_by_id(hotel_id: str) -> HotelSchema:
    return await HotelsDAO.get_by_id(int(hotel_id))


@router.get("/{location}")
async def get_hotels_by_location(location: str, date_from: date, date_to: date) -> list[HotelSchema]:
    # пользователь отправляет GET запрос со всеми данными (параметры функции) прямо в URL,
    # а API возвращает тип данных list[HotelSchema]
    # @app.get('/', response_model=list[HotelSchema]) также валидацию можно задавать в декораторе
    # rooms_left = await HotelsDAO
    pass