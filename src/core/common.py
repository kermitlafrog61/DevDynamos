from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_serializer, HttpUrl

from apps.auth.schemas import Profession, UserList
from apps.courses.schemas import CourseList, LectionList
from core.settings import settings


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    profession: Profession | None = None
    name: str | None = None
    last_name: str | None = None
    experience: int | None = None
    avatar_url: str | None = None
    about: str | None = None
    enrolled_courses: List[CourseList] = []
    owned_courses: List[CourseList] = []

    class Config:
        from_attributes = True

    @field_serializer('avatar_url')
    def avatar_url_serializer(self, value):
        return f'{settings.MEDIA_URL}{value}' if value else None


class CourseRead(BaseModel):
    id: int
    name: str
    about: str
    price: int
    photo_url: Optional[str]
    profession: Profession
    mentors: List[UserList] = []
    students: List[UserList] = []
    lections: List[LectionList] = []

    class Config:
        from_attributes = True

    @field_serializer('photo_url')
    def photo_url_serializer(self, value):
        return f'{settings.MEDIA_URL}{value}'


class LectionRead(BaseModel):
    id: int
    name: str
    about: str
    course: CourseRead
    video_link: HttpUrl
    homework_url: str

    @field_serializer('homework_url')
    def serializer_homework_url(self, value):
        return f'{settings.MEDIA_URL}{value}'

