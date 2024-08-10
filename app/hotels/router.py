from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import HotelSchema


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels & Rooms'],
)


# способ засунуть входящие данные (параметры функции) в модель для GET запроса
# обычный класс от BaseModel использовать нельзя, т.к. нет тела запроса
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


@router.get('')
async def get_all_hotels() -> list[HotelSchema]:
    return await HotelsDAO.get_all()


@router.get('/id/{hotel_id}')
async def get_hotel_by_id(hotel_id: str) -> HotelSchema:
    return await HotelsDAO.get_by_id(int(hotel_id))


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location(
        location: str,
        date_from: date = Query(..., description=f'Например {datetime.now().date()}'),
        date_to: date = Query(..., description=f'Например {datetime.now().date() + timedelta(days=7)}')
):  # если добавить валидацию данных list[HotelSchema], то не будет выдаваться столбец rooms_left, который не указан в схеме, но возвращается при запросе
    return await HotelsDAO.get_all_hotels_by_location(location, date_from, date_to)