from fastapi import status
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    if not pwd_context.verify(plain_password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password.")
