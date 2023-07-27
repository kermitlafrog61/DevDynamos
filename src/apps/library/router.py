from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from utils.token import get_current_user
from core.database import get_async_session
# from .schemas import OrderRead
from . import views


router = APIRouter(
    prefix="/api/v1/library"
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_courses(current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await views.get_courses(current_user=current_user, session=session)

@router.get("/{course_id}", status_code=status.HTTP_200_OK)
async def get_one_course(
        course_id: int, current_user: dict = Depends(get_current_user), 
        session: AsyncSession = Depends(get_async_session)
    ):
    return await views.get_one_course(course_id=course_id, current_user=current_user, session=session)

@router.post("/buy", status_code=status.HTTP_201_CREATED)
async def add_to_library(
        course_id: int, current_user: dict = Depends(get_current_user), 
        session: AsyncSession = Depends(get_async_session)
    ):
    return await views.add_to_library(course_id=course_id, current_user=current_user, session=session)