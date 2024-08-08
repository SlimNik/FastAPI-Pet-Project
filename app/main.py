from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.bookings.router import router as router_bookings
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users


app = FastAPI()

# монтирование отличается от подключения роутера тем, что подключается отдельное приложение со своим набором эндпойнтов
app.mount("/static", StaticFiles(directory="app/static"), "static")

# порядок подключения роутеров влияет на их порядок в документации
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)