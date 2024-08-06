from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.users.router import router as router_users


app = FastAPI()

# порядок подключения роутеров влияет на их порядок в документации
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)


class SHotel(BaseModel):
    name: str
    stars: int
    hotel_id: int


# способ засунуть входящие данные (параметры функции) в модель для GET запроса
# обычный класс от BaseModel использовать нельзя, т.к. нет тела запроса


