from typing import List

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)
from sqlalchemy.ext.asyncio import AsyncSession

from core.common import CourseRead
from core.database import get_async_session
from utils.media import save_image
from utils.token import get_current_user

from . import views
from .permissions import is_mentor_of_course, is_owner
from .schemas import CourseCreate, CourseList, CourseUpdate

router = APIRouter(
    prefix="/api/v1/courses",
)


@router.post(
    "/",
    response_model=CourseRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    name: str = Form(...),
    about: str = Form(...),
    profession_id: int = Form(...),
    price: int = Form(...),
    photo: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    """ Creating new course
    """
    await is_owner(current_user['id'], session)
    photo_url = await save_image(photo)

    course = CourseCreate(
        name=name,
        about=about,
        profession_id=profession_id,
        price=price,
        photo_url=photo_url
    )
    course = await views.create_course(course, session)
    return course


@router.get("/{course_id}", response_model=CourseRead)
async def get_course(course_id: int, session: AsyncSession = Depends(get_async_session)):
    """ Getting course by id
    """
    course = await views.show_course(course_id, session)
    return course


@router.get("/", response_model=List[CourseList])
async def get_courses(session: AsyncSession = Depends(get_async_session)):
    """ Getting all courses
    """
    courses = await views.list_courses(session)
    return courses


@router.put("/{course_id}", response_model=CourseRead)
async def update_course(
    course_id: int,
    name: str = Form(None),
    about: str = Form(None),
    profession_id: int = Form(None),
    price: int = Form(None),
    photo: UploadFile = File(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):

    await is_mentor_of_course(current_user['id'], course_id, session)
    course = CourseUpdate(
        name=name,
        about=about,
        profession_id=profession_id,
        price=price,
        photo=photo,
    )

    course = await views.course_update(course_id, course, session)
    return course
