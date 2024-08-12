from pathlib import Path

from PIL import Image

from app.tasks.celery_config import celery_app


@celery_app.tasks
def process_image(path: str):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized_1600x900 = img.resize((1600, 900))
    img_resized_1600x900.save(f"app/static/images/resized/resized_1600x900_{img_path.name}")
    img_resized_320x180 = img.resize((320, 180))
    img_resized_320x180.save(f"app/static/images/resized/resized_320x180_{img_path.name}")