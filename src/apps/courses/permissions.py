from sqlalchemy import select

from apps.auth.models import User
from apps.courses.models import Course


async def is_owner(user_id: int, session):
    q = select(User.is_owner).where(User.id == user_id)
    return await session.execute(q).scalar()


async def is_mentor_of_course(user_id: int, course_id: int, session):
    user = session.execute(select(User).where(User.id == user_id)).scalar()
    course = session.execute(select(Course).where(
        Course.id == course_id)).scalar()
    mentors = await course.awaitable_attrs.mentors
    return user in mentors
