from fastapi.exceptions import HTTPException
from sqlalchemy import select

from apps.auth.models import User
from apps.courses.models import Course


async def is_owner(user_id: int, session):
    result = await session.execute(select(User.is_owner).where(User.id == user_id))
    is_owner = result.scalar()
    if not is_owner:
        raise HTTPException(status_code=403, detail="You need to be an owner")


async def is_mentor_of_course(user_id: int, course_id: int, session):
    user = await session.execute(select(User).where(User.id == user_id))
    user = user.scalar()
    course = await session.execute(select(Course).where(
        Course.id == course_id))
    course = course.scalar()
    mentors = await course.awaitable_attrs.mentors
    if not user in mentors:
        raise HTTPException(status_code=403, detail="You need to be a mentor of this course")
