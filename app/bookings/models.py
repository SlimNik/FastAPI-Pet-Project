from datetime import date

from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Bookings(Base):
    __tablename__ = 'Bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    # миграции не получиться создать, пока не заданы все таблицы
    room_id: Mapped[int] = mapped_column(ForeignKey('Rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    date_from: Mapped[date] = mapped_column(nullable=False)
    date_to: Mapped[date] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"), nullable=False)
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"), nullable=False)