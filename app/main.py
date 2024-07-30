from fastapi import FastAPI, Query, Form


app = FastAPI()


# @app.get("/hotels/{hotel_name}/{hotel_id}")
# def get_hotels(hotel_id: int,
#                hotel_name: str,
#                date_from: datetime,
#                date_to: datetime,
#                stars: Optional[int] = Query(None, gt=0, lt=6),
#                sea_view: Optional[bool] = None
#                ):
#     return hotel_id, hotel_name, stars

@app.get('/calculate')
def get_page(num1: int = Form(ge=0, le=12), num2: int = Query(int, ge=0, le=100)):
    return {"result": num1 + num2}
