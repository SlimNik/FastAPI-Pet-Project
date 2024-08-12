from datetime import date

from pydantic import BaseModel


# схема (модель) данных, в данном случае брони, нужная для валидации входящих (тело запроса) и исходящих данных
class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        from_attributes = True