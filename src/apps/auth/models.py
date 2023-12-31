from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

try:
    from core.database import Base
    from apps.courses.models import course_mentors, course_students
except ModuleNotFoundError:
    from src.core.database import Base
    from src.apps.courses.models import course_mentors, course_students


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
    name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_owner = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    profession_id = Column(Integer, ForeignKey(
        "auth_profession.id"), nullable=True)
    experience = Column(Integer, default=0)
    activation_code = Column(String(length=36))
    avatar_url = Column(String, nullable=True)
    about = Column(String, nullable=True)

    profession = relationship(
        "Profession", uselist=False, back_populates="users")
    certificates = relationship("Certificate", back_populates="user")
    owned_courses: Mapped[list["Course"]] = relationship( # type: ignore
        secondary=course_mentors, back_populates="mentors")
    enrolled_courses: Mapped[list["Course"]] = relationship( # type: ignore
        secondary=course_students, back_populates="students")

    def __str__(self) -> str:
        return self.email
