from datetime import date

from sqlalchemy import select, literal_column, or_, and_, func
from sqlalchemy.orm import aliased

from app.bookings.models import BookingModel
from app.dao.base import BaseDAO
from app.database import async_session
from app.exceptions import RoomCannotBeBookedException
from app.hotels.models import HotelModel
from app.hotels.rooms.models import RoomModel


class HotelsDAO(BaseDAO):
    model = HotelModel

    @classmethod
    async def get_all_hotels_by_location(cls, location: str, date_from: date, date_to: date):
        async with async_session() as session:
            rooms_left_for_hotel = await cls.get_available_rooms_by_location(location, date_from, date_to)
            if not rooms_left_for_hotel:
                raise RoomCannotBeBookedException
            query = (
                select(HotelModel.__table__.columns, literal_column(str(rooms_left_for_hotel)).label('rooms_left'))
                .where(HotelModel.location == location)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_available_rooms_by_location(cls, location: str, date_from: date, date_to: date):
        r = aliased(RoomModel)
        bm = aliased(BookingModel)
        h = aliased(HotelModel)

        async with async_session() as session:
            """
            WITH booked_rooms AS (
                SELECT * FROM "Bookings" B RIGHT JOIN "Rooms" R ON R.id = B.room_id
                WHERE
                (date_from BETWEEN '2021-06-10' AND '2025-06-30') OR
                (date_from <= '2021-06-10' AND date_to >= '2021-06-10') OR
                (date_from <= '2025-06-30' AND date_to >= '2025-06-30')
            )
            """
            booked_rooms = (
                select(bm, r)
                .select_from(r).join(bm, r.id == bm.room_id, isouter=True)
                .where(
                    or_(
                        bm.date_from.between(date_from, date_to),
                        and_(bm.date_from <= date_from, bm.date_to >= date_from),
                        and_(bm.date_from <= date_to, bm.date_to >= date_to)
                    )
                )
            ).cte('booked_rooms')
            br = aliased(booked_rooms)
            """
            SELECT subq.rooms_quantity - SUM(subq.count) AS rooms_left
            FROM (
                SELECT H.location, H.rooms_quantity, COUNT(BR.room_id) AS count
                FROM booked_rooms BR
                RIGHT JOIN "Hotels" H ON BR.hotel_id = H.id
                GROUP BY H.location, H.rooms_quantity, BR.room_id
            ) AS subq
            GROUP BY subq.location, subq.rooms_quantity;
            """
            subq = (
                select(h.location, h.rooms_quantity, func.COUNT(br.c.id).label('count'))
                .select_from(h).join(br, br.c.hotel_id == h.id, isouter=True)
                .group_by(h.location, h.rooms_quantity, br.c.room_id)
            ).subquery('hotel_group')

            get_rooms_left_for_hotel = (
                select(subq.c.rooms_quantity - func.SUM(subq.c.count))
                .group_by(subq.c.location, subq.c.rooms_quantity)
                .having(and_(subq.c.location == location), subq.c.rooms_quantity - func.SUM(subq.c.count) > 0)
            )

            rooms_left_for_hotel = await session.execute(get_rooms_left_for_hotel)
            rooms_left_for_hotel: int = rooms_left_for_hotel.scalar()
            return rooms_left_for_hotel