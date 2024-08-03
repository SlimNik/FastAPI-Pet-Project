from app.DAO.base import BaseDAO
from app.bookings.models import Bookings


class BookingDAO(BaseDAO):
    # мы наследуем все методы из базового DAO
    # и указываем модель, для которой собираемся их использовать
    # DRY во всей красе
    model = Bookings
