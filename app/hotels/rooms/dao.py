from datetime import date

from sqlalchemy import select, and_, or_, func

from app.bookings.models import BookingModel
from app.dao.base import BaseDAO
from app.database import async_session
from app.hotels.rooms.models import RoomModel


class RoomsDAO(BaseDAO):
    model = RoomModel

    @classmethod
    async def get_available_rooms_by_hotel_id(cls, hotel_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM "Bookings"
            WHERE (date_from BETWEEN '2023-06-10' AND '2023-06-30') OR
                  (date_from <= '2023-06-10' AND date_to >= '2023-06-10') OR
                  (date_from <= '2023-06-30' AND date_to >= '2023-06-30')
        )
        SELECT R.quantity - COUNT(BR.room_id) AS rooms_left
        FROM "Rooms" R JOIN booked_rooms BR ON R.id = BR.room_id
        WHERE R.hotel_id = hotel_id
        GROUP BY R.quantity, BR.room_id
        """
        async with async_session() as session:
            booked_rooms = (
                select(BookingModel).where(
                    or_(
                        BookingModel.date_from.between(date_from, date_to),
                        and_(BookingModel.date_from <= date_from, BookingModel.date_to >= date_from),
                        and_(BookingModel.date_from <= date_to, BookingModel.date_to >= date_to)
                    )
                )
            ).cte('booked_rooms')

            get_rooms_left = (
                select((RoomModel.quantity - func.COUNT(booked_rooms.c.room_id)).label('rooms_left'))
                .select_from(RoomModel).join(booked_rooms, booked_rooms.c.room_id == RoomModel.id, isouter=True)
                .where(RoomModel.hotel_id == hotel_id)
                .group_by(RoomModel.quantity, booked_rooms.c.room_id)
            )

            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            return rooms_left