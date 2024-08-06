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
            SELECT * FROM "Bookings" B RIGHT JOIN "Rooms" R ON R.id = B.room_id
            WHERE
            (date_from BETWEEN '2021-06-10' AND '2025-06-30') OR
            (date_from <= '2021-06-10' AND date_to >= '2021-06-10') OR
            (date_from <= '2025-06-30' AND date_to >= '2025-06-30')
        )
        SELECT H.id, H.rooms_quantity - SUM(count) AS rooms_left
        FROM (
            SELECT H.id, H.rooms_quantity, COUNT(BR.room_id) AS count
            FROM booked_rooms BR
            RIGHT JOIN "Hotels" H ON BR.hotel_id = H.id
            GROUP BY H.id, H.rooms_quantity, BR.room_id
            ) AS H
        GROUP BY H.id, H.rooms_quantity
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