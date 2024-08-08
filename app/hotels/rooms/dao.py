from datetime import date

from sqlalchemy import select, and_, or_, func, literal_column
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import coalesce

from app.bookings.models import BookingModel
from app.dao.base import BaseDAO
from app.database import async_session
from app.hotels.rooms.models import RoomModel


class RoomsDAO(BaseDAO):
    model = RoomModel

    @classmethod
    async def get_all_by_hotel_id(cls, hotel_id: int, date_from: date, date_to: date):
        rooms = aliased(RoomModel)
        bookings = aliased(BookingModel)

        async with async_session() as session:
            """
            WITH booked_rooms AS (
                SELECT * FROM "Bookings" B RIGHT JOIN "Rooms" R ON R.id = B.room_id
                WHERE (date_from BETWEEN '2021-06-10' AND '2025-06-30') OR
                      (date_from <= '2021-06-10' AND date_to >= '2021-06-10') OR
                      (date_from <= '2025-06-30' AND date_to >= '2025-06-30')
            )
            """
            booked_rooms = (
                select(bookings, rooms)
                .select_from(rooms).join(bookings, rooms.id == bookings.room_id, isouter=True)
                .where(
                    or_(
                        bookings.date_from.between(date_from, date_to),
                        and_(bookings.date_from <= date_from, bookings.date_to >= date_from),
                        and_(bookings.date_from <= date_to, bookings.date_to >= date_to)
                    )
                )
            ).cte('booked_rooms')
            b_rooms = aliased(booked_rooms)
            """
            SELECT R.*, COALESCE(H.rooms_left, R.quantity) AS rooms_left
            FROM "Rooms" R
            LEFT JOIN (
                SELECT BR.room_id, BR.quantity - COUNT(BR.room_id) AS rooms_left
                FROM booked_rooms BR
                GROUP BY BR.room_id, BR.quantity
            ) AS H ON R.id = H.room_id
            ORDER BY R.id;
            """
            subq = (
                select(
                    b_rooms.c.room_id,
                    (b_rooms.c.quantity - func.COUNT(b_rooms.c.room_id)).label('rooms_left')
                )
                .group_by(b_rooms.c.room_id, b_rooms.c.quantity)
            ).subquery()

            query = (
                select(
                    rooms.id,
                    rooms.hotel_id,
                    rooms.name,
                    rooms.description,
                    rooms.services,
                    rooms.price,
                    rooms.quantity,
                    rooms.image_id,
                    literal_column(f'{(date_to - date_from).days} * price').label('total_cost'),
                    coalesce(subq.c.rooms_left, rooms.quantity).label('rooms_left')
                )
                .select_from(rooms).join(subq, rooms.id == subq.c.room_id, isouter=True)
                .where(rooms.hotel_id == hotel_id)
            )

            result = await session.execute(query)
            return result.mappings().all()