from typing import List

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from utils.media import save_image

from . import views
from .schemas import CourseCreate, CourseRead, CourseUpdate, CourseList

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
    session: AsyncSession = Depends(get_async_session)
):
    """ Creating new course
    """
    # FIXME: add validation that user is an owner
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
    course = await views.get_course(course_id, session)
    return course


@router.get("/", response_model=List[CourseList])
async def get_courses(session: AsyncSession = Depends(get_async_session)):
    """ Getting all courses
    """
    courses = await views.list_courses(session)
    return courses
