from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, field_serializer

from apps.auth.schemas import Profession
from core.settings import settings


class CourseCreate(BaseModel):
    name: str
    about: str
    profession_id: int
    price: int
    photo_url: str


class CourseUpdate(BaseModel):
    name: Optional[str]
    about: Optional[str]
    price: Optional[int]
    photo_url: Optional[UploadFile]


class CourseRead(BaseModel):
    id: int
    name: str
    about: str
    price: int
    photo_url: str
    profession: Profession

    class Config:
        from_attributes = True

    @field_serializer('photo_url')
    def photo_url_serializer(self, value):
        return f'{settings.MEDIA_URL}{value}'


class CourseList(BaseModel):
    id: int
    name: str
    about: str
    price: int
    photo_url: str
