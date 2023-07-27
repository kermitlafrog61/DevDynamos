from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from apps.courses.models import Course
from .models import Library


async def get_courses(current_user: dict, session: AsyncSession):
    query = await session.execute(select(Library).where(Library.user_id == current_user["id"]))
    return query.scalars().all()

async def get_one_course(course_id: int, current_user: dict, session: AsyncSession):
    try:
        one_saved_course = await session.get(Library, course_id)
        course = await session.get(Course, one_saved_course.course_id)
        return {
            "data": one_saved_course,
            "response": course,
        }
    except AttributeError:
        return {
            "response": "There's no course with this id",
            "status": status.HTTP_400_BAD_REQUEST,
        }

async def add_to_library(course_id: int, current_user: dict, session: AsyncSession):
    query = await session.execute(select(Library).where(Library.course_id == course_id))
    q = query.scalars().all()
    
    try:
        if q[0].course_id:
            if q[0].user_id == current_user["id"] or q[0].course_id == course_id:
                return {"response": "The course is already purchased"}
            elif q[0].user_id != current_user["id"]:
                await session.execute(insert(Library).values(user_id = current_user["id"], course_id = course_id))
                await session.commit()
                return await get_courses(current_user=current_user, session=session)
            return {"response": "The course is already purchased"}
    except IndexError:
        try:
            await session.execute(insert(Library).values(user_id = current_user["id"], course_id = course_id))
            await session.commit()
            return await get_courses(current_user=current_user, session=session)
        except IntegrityError:
            return {"response": "There's no course with this id"}