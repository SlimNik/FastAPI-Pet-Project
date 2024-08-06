from pydantic import BaseModel


class HotelSchema(BaseModel):
    id: int
    name: str
    location: str
    services: dict
    rooms_quantity: int
    image_id: int