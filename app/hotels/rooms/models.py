from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Rooms(Base):
    __tablename__ = 'Rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('Hotels.id'), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[dict] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]