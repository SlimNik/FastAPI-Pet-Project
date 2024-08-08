from shutil import copyfileobj

from fastapi import APIRouter, UploadFile


router = APIRouter(
    prefix="/images",
    tags=["Upload images"]
)


@router.post("/hotels")
async def add_hotels_image(file_index: int, uploaded_file: UploadFile) -> None:
    with open(f"app/static/images/{file_index}.webp", "wb+") as file_obj:
        copyfileobj(uploaded_file.file, file_obj)


@router.post("/rooms")
async def add_rooms_image(file_index: int, uploaded_file: UploadFile) -> None:
    with open(f"app/static/images/room{file_index}.webp", "wb+") as file_obj:
        copyfileobj(uploaded_file.file, file_obj)