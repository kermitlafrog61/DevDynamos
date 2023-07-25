from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel

from apps.auth.schemas import Profession


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
        orm_mode = True


class CourseList(BaseModel):
    id: int
    name: str
    about: str
    price: int
    photo_url: str
