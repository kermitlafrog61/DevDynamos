import re

from pydantic import BaseModel, field_validator, field_serializer

from core.settings import settings


class Profession(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: int
    email: str
    username: str
    profession: Profession | None = None
    name: str | None = None
    last_name: str | None = None
    experience: int | None = None
    avatar_url: str | None = None
    about: str | None = None

    class Config:
        from_attributes = True

    @field_serializer('avatar_url')
    def avatar_url_serializer(self, value):
        return f'{settings.MEDIA_URL}{value}' if value else None


class UserCreate(BaseModel):
    email: str
    username: str
    password: str

    @field_validator("email")
    def validate_email(cls, email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        raise ValueError("Invalid email")


class ResetPassword(BaseModel):
    email: str


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
    avatar_url: str | None = None
    about: str | None = None
