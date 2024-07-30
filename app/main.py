from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query


app = FastAPI()


@app.get("/hotels/{hotel_name}/{hotel_id}")
def get_hotels(hotel_id: int,
               hotel_name: str,
               date_from: datetime,
               date_to: datetime,
               stars: Optional[int] = Query(None, gt=0, lt=6),
               sea_view: Optional[bool] = None
               ):
    return hotel_id, hotel_name, stars
