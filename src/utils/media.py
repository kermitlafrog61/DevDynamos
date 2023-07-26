import uuid

from fastapi import UploadFile

from core.settings import settings


async def save_image(file: UploadFile):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    with open(f'{settings.MEDIA_ROOT}/{file.filename}', 'wb') as f:
        f.write(contents)

    return file.filename
