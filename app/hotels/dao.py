from datetime import date

from sqlalchemy import select, or_, and_, func
from sqlalchemy.orm import aliased

from app.bookings.models import BookingModel
from app.dao.base import BaseDAO
from app.database import async_session
from app.hotels.models import HotelModel
from app.hotels.rooms.models import RoomModel


class HotelsDAO(BaseDAO):
    model = HotelModel

    @classmethod
    async def get_all_hotels_by_location(cls, location: str, date_from: date, date_to: date):
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
            SELECT H.*, filtered_hotel_group.rooms_left
            FROM (
                SELECT
                    hotel_group.hotel_id,
                    hotel_group.location,
                    hotel_group.rooms_quantity - SUM(hotel_group.count) AS rooms_left
                FROM (
                    SELECT H.id AS hotel_id, H.location, H.rooms_quantity, COUNT(BR.room_id) AS count
                    FROM booked_rooms BR
                    RIGHT JOIN "Hotels" H ON BR.hotel_id = H.id
                    GROUP BY H.id, H.location, H.rooms_quantity, BR.room_id
                ) AS hotel_group
                GROUP BY
                    hotel_group.hotel_id,
                    hotel_group.location,
                    hotel_group.rooms_quantity
                HAVING
                    hotel_group.location LIKE '%Алтай%' AND
                    hotel_group.rooms_quantity - SUM(hotel_group.count) > 0) AS filtered_hotel_group
            LEFT JOIN "Hotels" H ON H.id = filtered_hotel_group.hotel_id;
            """
            hotel_group = (
                select(
                    h.id.label('hotel_id'),
                    h.location,
                    h.rooms_quantity, func.COUNT(br.c.id).label('count')
                )
                .select_from(h).join(br, br.c.hotel_id == h.id, isouter=True)
                .group_by(
                    h.id,
                    h.location,
                    h.rooms_quantity,
                    br.c.room_id
                )
            ).subquery('hotel_group')

            filtered_hotel_group = (
                select(
                    hotel_group.c.hotel_id,
                    hotel_group.c.location,
                    (hotel_group.c.rooms_quantity - func.SUM(hotel_group.c.count)).label('rooms_left')
                )
                .group_by(
                    hotel_group.c.hotel_id,
                    hotel_group.c.location,
                    hotel_group.c.rooms_quantity
                )
                .having(
                    and_(
                        hotel_group.c.location.ilike(f'%{location}%'),
                        hotel_group.c.rooms_quantity - func.SUM(hotel_group.c.count) > 0
                    )
                )
            ).subquery('filtered_hotel_group')

            query = (
                select(
                    h.id,
                    h.name,
                    h.location,
                    h.services,
                    h.rooms_quantity,
                    h.image_id,
                    filtered_hotel_group.c.rooms_left
                )
                .select_from(filtered_hotel_group).join(h, h.id == filtered_hotel_group.c.hotel_id, isouter=True)
            )

            result = await session.execute(query)
            return result.mappings().all()