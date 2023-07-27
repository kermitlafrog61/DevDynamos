from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from utils.asyncio import await_awaitable_attrs
from utils.media import delete_image, save_image

from .models import Course, course_students
from .schemas import CourseCreate, CourseUpdate


async def create_course(course: CourseCreate, session: AsyncSession):
    new_course = Course(**course.model_dump())
    session.add(new_course)
    await session.commit()
    await session.refresh(new_course)
    await await_awaitable_attrs(new_course)
    return new_course


async def get_course_by_id(course_id: int, session: AsyncSession):
    course = await session.get(Course, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found")
    return course


async def show_course(course_id: int, session: AsyncSession):
    course = await get_course_by_id(course_id, session)
    await await_awaitable_attrs(course)
    return course


async def list_courses(session: AsyncSession):
    q = await session.execute(select(Course))
    courses = q.scalars().all()
    return courses


async def course_update(
        course_id: int, course_data: CourseUpdate, session: AsyncSession):
    """ Updating user's data """
    data = course_data.model_dump(exclude_none=True)
    course = await get_course_by_id(course_id, session)
    for key, value in data.items():
        if key == 'photo':
            if course.photo_url is not None:
                delete_image(course.photo_url)
            key = 'photo_url'
            value = await save_image(value)
        setattr(course, key, value)

    session.add(course)
    await session.commit()
    await session.refresh(course)
    await await_awaitable_attrs(course)
    return course


async def add_user_to_course(course_id: int, user_id: int, session: AsyncSession):
    query = course_students.insert().values(course_id=course_id, user_id=user_id)

    try:
        await session.execute(query)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} is already in course")

    await session.commit()
    return await show_course(course_id, session)
