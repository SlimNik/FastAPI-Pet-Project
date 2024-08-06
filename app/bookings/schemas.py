from datetime import date

from pydantic import BaseModel


# схема (модель) данных, в данном случае брони, нужная для валидации входящих (тело запроса) и исходящих данных
class SBookings(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int