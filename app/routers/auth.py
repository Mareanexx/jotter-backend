from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.wrapped_response import WrappedResponse
from app.models.profile import Profile
from app.schemas.user import AuthResponse, UserLogin, UserCreate
from app.core.database import get_db
from app.models.user import User, UserStatus
from passlib.hash import bcrypt
from app.core.security import create_access_token
from app.services.user import create_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=WrappedResponse[AuthResponse])
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=403, detail="User is inactive or banned")

    profile_result = await db.execute(select(Profile.id).where(Profile.user_uuid == user.uuid))
    profile_id = profile_result.scalar_one_or_none()

    if profile_id is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    token = create_access_token({"user_id": str(user.uuid)})
    return WrappedResponse(
        message="Login successful",
        data=AuthResponse(access_token=token, user_uuid=user.uuid, profile_id=profile_id)
    )


@router.post("/register", response_model=WrappedResponse[AuthResponse])
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    profile = await create_user(user_data, db)

    token = create_access_token({"user_id": str(profile.user_uuid)})
    return WrappedResponse(
        message="Register successful",
        data=AuthResponse(access_token=token, user_uuid=profile.user_uuid, profile_id=profile.id)
    )
