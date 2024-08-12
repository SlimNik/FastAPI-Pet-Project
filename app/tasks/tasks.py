import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_config import celery_app
from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def process_image(path: str):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized_1600x900 = img.resize((1600, 900))
    img_resized_1600x900.save(f"app/static/images/resized/resized_1600x900_{img_path.name}")
    img_resized_320x180 = img.resize((320, 180))
    img_resized_320x180.save(f"app/static/images/resized/resized_320x180_{img_path.name}")


@celery_app.task
def send_booking_confirmation_email(
        booking: dict,
        # email_to: EmailStr
):
    msg_content = create_booking_confirmation_template(booking, settings.SMTP_USER)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)