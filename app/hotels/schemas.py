from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: dict
    rooms_quantity: int
    image_id: int