from datetime import date

from sqlalchemy import select, and_, or_, func, insert
from sqlalchemy.orm import aliased

from app.bookings.models import BookingModel
from app.dao.base import BaseDAO
from app.database import async_session
from app.hotels.rooms.models import RoomModel


class BookingsDAO(BaseDAO):
    # мы наследуем все методы из базового dao
    # и указываем модель, для которой собираемся их использовать
    # DRY во всей красе
    model = BookingModel

    @staticmethod
    async def get_available_rooms_by_room_id(room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM "Bookings"
            WHERE room_id = 1 AND
            (date_from BETWEEN '2023-06-10' AND '2023-06-30') OR
            (date_from <= '2023-06-10' AND date_to >= '2023-06-10') OR
            (date_from <= '2023-06-30' AND date_to >= '2023-06-30')
        )
        SELECT R.quantity - COUNT(BR.room_id) AS rooms_left
        FROM "Rooms" R JOIN booked_rooms BR ON R.id = BR.room_id
        WHERE R.id = 1
        GROUP BY R.quantity, BR.room_id
        """
        async with async_session() as session:
            booked_rooms = (
                select(BookingModel).where(
                    and_(
                        BookingModel.room_id == room_id,
                        or_(
                            BookingModel.date_from.between(date_from, date_to),
                            and_(BookingModel.date_from <= date_from, BookingModel.date_to >= date_from),
                            and_(BookingModel.date_from <= date_to, BookingModel.date_to >= date_to)
                        )
                    )
                )
            ).cte('booked_rooms')

            get_rooms_left = (
                select((RoomModel.quantity - func.COUNT(booked_rooms.c.room_id)).label('rooms_left'))
                .select_from(RoomModel).join(booked_rooms, booked_rooms.c.room_id == RoomModel.id, isouter=True)
                .where(RoomModel.id == room_id)
                .group_by(RoomModel.quantity, booked_rooms.c.room_id)
            )

            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            return rooms_left

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        rooms_left = await cls.get_available_rooms_by_room_id(room_id, date_from, date_to)
        if rooms_left:
            async with async_session() as session:
                get_price = select(RoomModel.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(BookingModel).values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(BookingModel)  # возвращает схему

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()  # т.к. возвращается одна схема pydantic
        return None

    @classmethod
    async def get_all(cls, user_id: int):
        async with async_session() as session:
            bm = aliased(BookingModel)
            rm = aliased(RoomModel)
            query = (
                select(
                    bm.room_id,
                    bm.user_id,
                    bm.date_from,
                    bm.date_to,
                    bm.price,
                    bm.total_cost,
                    bm.total_days,
                    rm.image_id,
                    rm.name,
                    rm.description,
                    rm.services
                )
                .select_from(bm).join(rm, rm.id == bm.room_id)
                .where(bm.user_id == user_id)
            )
            result = await session.execute(query)
            return result.mappings().all()