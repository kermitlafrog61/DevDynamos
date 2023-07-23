from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        func)
from sqlalchemy.orm import relationship

try:
    from core.database import Base
except ModuleNotFoundError:
    from src.core.database import Base


metadata = Base.metadata


class Profession(Base):
    __tablename__ = "auth_profession"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="profession")

    def __str__(self) -> str:
        return self.name


class Certificate(Base):
    __tablename__ = "auth_certificate"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    # photo = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("auth_account.id"))

    user = relationship("User", back_populates="certificates")


class User(Base):
    __tablename__ = "auth_account"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password: str = Column(String(length=75), nullable=False)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_owner = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    profession_id = Column(Integer, ForeignKey("auth_profession.id"))
    experience = Column(Integer, default=0)
    activation_code = Column(String(length=36))
    # avatar = Column(String)
    about = Column(String)

    profession = relationship("Profession", uselist=False, back_populates="users")
    certificates = relationship("Certificate", back_populates="user")

    def __str__(self) -> str:
        return self.email
