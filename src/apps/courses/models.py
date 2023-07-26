from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

try:
    from core.database import Base
except ModuleNotFoundError:
    from src.core.database import Base


metadata = Base.metadata


course_mentors = Table(
    "courses_course_mentors",
    metadata,
    Column("course_id", ForeignKey("courses_course.id"), primary_key=True),
    Column("user_id", ForeignKey("auth_account.id"), primary_key=True),
)

course_students = Table(
    "courses_course_students",
    metadata,
    Column("course_id", ForeignKey("courses_course.id"), primary_key=True),
    Column("user_id", ForeignKey("auth_account.id"), primary_key=True),
)


class Course(Base):
    __tablename__ = "courses_course"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    about = Column(String, nullable=False)
    profession_id = Column(Integer, ForeignKey("auth_profession.id"))
    price = Column(Integer, nullable=True)
    photo_url = Column(String)

    profession = relationship("Profession")
    lections = relationship("Lection", back_populates="course")
    mentors: Mapped[list['User']] = relationship(secondary=course_mentors, # type: ignore
                           back_populates="owned_courses")
    students: Mapped[list['User']] = relationship(secondary=course_students, # type: ignore
                            back_populates="enrolled_courses")

    def __str__(self) -> str:
        return self.name


class Lection(Base):
    __tablename__ = "courses_lection"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    about = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey("courses_course.id"))
    video_link = Column(String)
    homework_url = Column(String)

    course = relationship("Course", back_populates="lections")

    def __str__(self) -> str:
        return self.name
