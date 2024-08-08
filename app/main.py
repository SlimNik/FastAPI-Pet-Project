from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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

# источники, из которых через браузер можно обращаться API
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # позволить сохранять куки
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],  # в продакшене лучше указать явно
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)