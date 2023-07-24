import re

from pydantic import BaseModel, field_validator


class Profession(BaseModel):
    name: str

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: int
    email: str
    username: str
    name: str
    last_name: str
    profession: Profession
    experience: int
    # avatar: str = None
    about: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    name: str
    last_name: str
    profession_id: int
    experience: int
    # avatar: str = None
    about: str

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
