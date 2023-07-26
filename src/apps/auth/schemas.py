from fastapi import UploadFile
from pydantic import BaseModel, field_serializer, EmailStr

from core.settings import settings


class Profession(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class ResetPassword(BaseModel):
    email: EmailStr


class PasswordRecovery(ResetPassword):
    recovery_code: int
    new_password: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class UserUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    profession_id: int | None = None
    experience: int | None = None
    avatar: UploadFile | None = None
    about: str | None = None


class UserList(BaseModel):
    id: int
    email: EmailStr
    username: str
    name: str | None = None
    last_name: str | None = None
    experience: int | None = None
    avatar_url: str | None = None

    @field_serializer('avatar_url')
    def avatar_url_serializer(self, value):
        return f'{settings.MEDIA_URL}{value}' if value else None
