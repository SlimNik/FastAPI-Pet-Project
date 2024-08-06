from app.dao.base import BaseDAO
from app.hotels.models import HotelModel


class HotelsDAO(BaseDAO):
    model = HotelModel