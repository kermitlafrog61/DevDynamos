from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

try:
    from core.database import Base
except ModuleNotFoundError:
    from src.core.database import Base


metadata = Base.metadata


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
