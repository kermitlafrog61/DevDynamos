from typing import Optional, List

from fastapi import UploadFile
from pydantic import BaseModel, field_serializer

from core.settings import settings


class LectionList(BaseModel):
    id: int
    name: str
    about: str


class CourseCreate(BaseModel):
    name: str
    about: str
    profession_id: int
    price: int
    photo_url: str


class CourseUpdate(BaseModel):
    name: Optional[str]
    about: Optional[str]
    profession_id: Optional[int]
    price: Optional[int]
    photo_url: Optional[UploadFile]


class CourseList(BaseModel):
    id: int
    name: str
    about: str
    price: int
    photo_url: str

    @field_serializer('photo_url')
    def photo_url_serializer(self, value):
        return f'{settings.MEDIA_URL}{value}'
