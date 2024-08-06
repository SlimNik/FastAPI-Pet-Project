from fastapi import APIRouter


router = APIRouter(
    prefix='/hotels',
    tags=['Hotels & Rooms'],
)


@router.get("")
def get_hotels():
    pass