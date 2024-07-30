from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel


app = FastAPI()


# схема (модель) данных, в данном случае брони, нужная для валидации входящих (тело запроса) и исходящих данных
class SBooking(BaseModel):
    hotel_id: int
    date_from: datetime
    date_to: datetime


class SHotel(BaseModel):
    name: str
    stars: int
    hotel_id: int


# способ засунуть входящие данные (параметры функции) в модель для GET запроса
# обычный класс от BaseModel использовать нельзя, т.к. нет тела запроса
class HotelSearchArgs:
    def __init__(self,
                 hotel_id: int,
                 hotel_name: str,
                 date_from: datetime,
                 date_to: datetime,
                 stars: Optional[int] = Query(None, gt=0, lt=6),
                 sea_view: Optional[bool] = None
                 ):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.sea_view = sea_view


@app.get("/hotels/{hotel_name}/{hotel_id}")
def get_hotels(
        #  hotel_id: int,
        # hotel_name: str,
        # date_from: datetime,
        # date_to: datetime,
        # stars: Optional[int] = Query(None, gt=0, lt=6),
        # sea_view: Optional[bool] = None,
        search_args: HotelSearchArgs = Depends()
) -> list[SHotel]:
    # пользователь отправляет GET запрос со всеми данными (параметры функции) прямо в URL,
    # а API возвращает тип данных list[SHotel]
    # также валидацию можно задавать в декораторе @app.get('/', response_model=list[SHotel])
    hotels = [
        {
            "name": "Hotel1",
            "stars": 5,
            "hotel_id": 5325
        },
        {
            "name": "Hotel2",
            "stars": 3,
            "hotel_id": 515
        }
    ]
    return hotels


@app.post("/booking")
def add_booking(new_booking: SBooking):
    pass
