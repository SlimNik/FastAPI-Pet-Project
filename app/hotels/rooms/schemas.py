from pydantic import BaseModel


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: dict
    quantity: int
    image_id: int