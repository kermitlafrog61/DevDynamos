from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
try:
    from core.database import Base
except ModuleNotFoundError:
    from src.core.database import Base

metadata = Base.metadata


class Library(Base):
    __tablename__ = "library_courses"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_account.id"))
    course_id = Column(Integer, ForeignKey("courses_course.id"))
    
    account = relationship("User", back_populates="library")
    course = relationship("Course", back_populates="library")
    
    def __str__(self):
        return self.course_id