from shutil import copyfileobj

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_image


router = APIRouter(
    prefix="/images",
    tags=["Upload images"]
)


@router.post("/hotels")
async def add_hotels_image(file_index: int, uploaded_file: UploadFile) -> None:
    img_path = f"app/static/images/hotels/hotel{file_index}.webp"
    with open(img_path, "wb+") as file_obj:
        copyfileobj(uploaded_file.file, file_obj)
    process_image.delay(img_path)


@router.post("/rooms")
async def add_rooms_image(file_index: int, uploaded_file: UploadFile) -> None:
    img_path = f"app/static/images/rooms/room{file_index}.webp"
    with open(img_path, "wb+") as file_obj:
        copyfileobj(uploaded_file.file, file_obj)
    process_image.delay(img_path)