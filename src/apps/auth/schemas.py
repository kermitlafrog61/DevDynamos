from typing import List

from pydantic import BaseModel


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


class ResetPassword(BaseModel):
    email: str


class PasswordRecovery(ResetPassword):
    recovery_code: int
    new_password: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
