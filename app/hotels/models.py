from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotels(Base):
    __tablename__ = 'Hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[dict] = mapped_column(JSON, nullable=True)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]