from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from apps.courses.models import Course, course_mentors, course_students


async def is_owner(user_id: int, session):
    result = await session.execute(select(User.is_owner).where(User.id == user_id))
    is_owner = result.scalar()
    if not is_owner:
        raise HTTPException(status_code=403, detail="You need to be an owner")


async def is_mentor_of_course(user_id: int, course_id: int, session: AsyncSession):
    statement = select(course_mentors).where(
        (course_mentors.c.course_id == course_id) &
        (course_mentors.c.user_id == user_id)
    )
    result = await session.execute(statement)

    if result.fetchone() is None:
        raise HTTPException(
            status_code=403, detail="You need to be a mentor of this course")


async def is_mentor_or_student_of_course(user_id: int, course_id: int, session: AsyncSession):
    mentor_statement = select(course_mentors).where(
        (course_mentors.c.course_id == course_id) &
        (course_mentors.c.user_id == user_id)
    )
    student_statement = select(course_students).where(
        (course_students.c.course_id == course_id) &
        (course_students.c.user_id == user_id)
    )

    mentors = await session.execute(mentor_statement)
    students = await session.execute(student_statement)

    if mentors.fetchone() is None and students.fetchone() is None:
        raise HTTPException(
            status_code=403, detail="You need to be a mentor or student of this course")
