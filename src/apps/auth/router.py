from fastapi import APIRouter, Depends, HTTPException, status, File, Form, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from utils.hasher import verify_password
from utils.token import create_access_token, get_current_user

from . import views
from .schemas import (PasswordChange, PasswordRecovery, ResetPassword,
                      UserCreate, UserRead)

router = APIRouter(
    prefix="/api/v1/auth",
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def profile_register(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """ User registration
    """
    try:
        # creating user in database
        return await views.create_user(user, session)
    except IntegrityError:
        """ Handling 'existing user' exception
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered.")


@router.post("/confirm")
async def profile_activation(activation_code: str, session: AsyncSession = Depends(get_async_session)):
    """ Account activation
    """
    return await views.activate_account(code=activation_code, session=session)


@router.post("/login")
async def profile_login(body: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    """ Account login
    """
    user = await views.get_user_by_email(email=body.username, session=session)
    password = user.hashed_password
    verify_password(plain_password=body.password, hashed_password=password)

    if user.is_active == True:
        # creating token
        access_token = await create_access_token(
            data={
                "sub": {
                    "id": user.id,
                    "email": user.email,
                },
            },
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "email": user.email,
                "username": user.username,
            }
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Inactive account.")


@router.post("/reset-password")
async def profile_recovery(request: ResetPassword, session: AsyncSession = Depends(get_async_session)):
    try:
        return await views.create_recovery_code(email=request.email, session=session)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists.")


@router.post("/password-recovery")
async def profile_set_new_password(
    request: PasswordRecovery,
    session: AsyncSession = Depends(get_async_session)
):
    """ Updating user password """
    return await views.set_new_password(
        user_id=request.email, recovery_code=request.recovery_code,
        new_password=request.new_password, session=session
    )


@router.post("/password-change")
async def profile_password_change(
    request: PasswordChange,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """ Changing user password """
    try:
        user = await views.get_user_by_id(email=current_user['id'], session=session)
        verify_password(
            plain_password=request.old_password, hashed_password=user.hashed_password)

        return await views.change_password(
            user_id=current_user['id'],
            new_password=request.new_password, session=session
        )
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email.")


@router.get('/users/me', response_model=UserRead)
async def get_current_user_info(current_user: dict = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    user = await views.show_user_by_id(id=current_user['id'], session=session)
    return user


@router.put('/users/me', response_model=UserRead)
async def update_current_user_info(
        name: str | None = Form(None),
        last_name: str | None = Form(None),
        profession_id: int | None = Form(None),
        experience: int | None = Form(None),
        avatar: UploadFile | None = File(None),
        about: str | None = Form(None),
        current_user: dict = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)):
    user = await views.user_update(id=current_user['id'], session=session)
    return user
