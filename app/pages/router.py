from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.hotels.rooms.router import get_rooms_by_hotel_id, get_all_rooms
from app.hotels.router import get_hotels_by_location, get_all_hotels


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/hotels")
async def get_hotels_page(
        request: Request,
        hotels=Depends(get_hotels_by_location),
        all_hotels=Depends(get_all_hotels)
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={
            "request": request,
            "hotels": hotels,
            "all_hotels": all_hotels
        }
    )


@router.get("/rooms")
async def get_rooms_page(
        request: Request,
        rooms=Depends(get_rooms_by_hotel_id),
        all_rooms=Depends(get_all_rooms)
):
    return templates.TemplateResponse(
        name="rooms.html",
        context={
            "request": request,
            "rooms": rooms,
            "all_rooms": all_rooms
        }
    )