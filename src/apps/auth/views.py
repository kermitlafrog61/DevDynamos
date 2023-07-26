import uuid

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from utils.hasher import hash_password

from .tasks import send_email_confirmation, send_email_recovery
from .models import User
from .schemas import UserCreate, UserUpdate


async def get_user_by_id(id: int, session: AsyncSession):
    """ Searching user in database by id """
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(email: str, session: AsyncSession):
    """ Searching user in database by email """
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def show_user(id: int, session: AsyncSession):
    """ Showing user """
    user = await get_user_by_id(id=id, session=session)
    await user.awaitable_attrs.profession
    return user


async def create_activation_code(email: str, session: AsyncSession) -> str:
    """ Creating activation code for user """
    activation_code = str(uuid.uuid4())
    stmt = (
        update(User).
        where(User.email == email).
        values(activation_code=activation_code)
    )
    await session.execute(stmt)
    try:
        await session.commit()
    except IndexError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {
            "message": "Current User not found"
        })

    return activation_code


async def check_activation_code(code: str, session: AsyncSession):
    """ Checking activation code for user """
    query = select(User).where(User.activation_code == code)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.activation_code = ""
    await session.commit()
    return user


async def create_user(user: UserCreate, session: AsyncSession):
    """ Creating user with email sending
    """
    data = user.model_dump()
    data['hashed_password'] = hash_password(data.pop('password'))
    new_user = User(**data)
    await create_activation_code(email=new_user.email, session=session)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    await new_user.awaitable_attrs.profession

    send_email_confirmation.delay(
        new_user.email, new_user.activation_code)
    return new_user


async def activate_account(code: str, session: AsyncSession):
    """ Activating user account
    """
    await check_activation_code(code=code, session=session)
    stmt = (
        update(User).
        where(User.activation_code == code).
        values(is_active=True)
    )
    await session.execute(stmt)

    try:
        await session.commit()
    except IndexError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, {
            "message": "Incorrect code, please try again."
        })

    return {
        "message": "Account activated successfully!"
    }


async def create_recovery_code(email: str, session: AsyncSession):
    """ Creating recovery code to reset user password
    """
    activation_code = await create_activation_code(email=email, session=session)
    send_email_recovery.delay(user_email=email, code=activation_code)
    return {
        "message": "We've sent a recovery code, please check your email."
    }


async def set_new_password(
    user_id: int, recovery_code: int, new_password: str,
    session: AsyncSession
):
    """ Seting the user's new password """
    await check_activation_code(code=recovery_code, session=session)
    stmt = (
        update(User).
        where(User.id == user_id).
        values(hashed_password=hash_password(new_password))
    )
    await session.execute(stmt)
    try:
        await session.commit()
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect email or you've already reset your password. Please, click on 'send recovery code'."
        )
    return {
        "message": "Password has been reset successfully."
    }


async def change_password(
    user_id: int, new_password: str,
    session: AsyncSession
):
    """ Changing the user's old password """
    stmt = (
        update(User).
        where(User.id == user_id).
        values(hashed_password=hash_password(new_password))
    )
    await session.execute(stmt)
    await session.commit()
    return {
        "message": "Password has been updated successfully."
    }


async def user_update(
    user_id: int, user_data: UserUpdate, session: AsyncSession):
    """ Updating user's data """
    data = user_data.model_dump(exclude_none=True)
    user = await get_user_by_id(id=user_id, session=session)
    for key, value in data.items():
        setattr(user, key, value)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    await user.awaitable_attrs.profession
    return user
