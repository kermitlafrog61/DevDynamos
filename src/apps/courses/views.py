from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Course
from .schemas import CourseCreate, CourseUpdate


async def create_course(course: CourseCreate, session: AsyncSession):
    new_course = Course(**course.model_dump())
    session.add(new_course)
    await session.commit()
    await session.refresh(new_course)
    await new_course.awaitable_attrs.profession
    return new_course


async def get_course(course_id: int, session: AsyncSession):
    course = await session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Course with id {course_id} not found')
    await course.awaitable_attrs.profession
    return course


async def list_courses(session: AsyncSession):
    q = await session.execute(select(Course))
    courses = q.scalars().all()
    return courses
