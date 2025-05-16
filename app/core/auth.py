from typing import Type

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.profile import Profile
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_profile(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> Profile:  # Используем прямо Profile вместо Type[Profile]
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None or "user_id" not in payload:
        raise credentials_exception

    # Ищем сначала User по UUID из токена
    user_uuid = payload["user_id"]
    user = await db.execute(select(User).where(User.uuid == user_uuid))
    user = user.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    # Затем находим связанный Profile
    profile = await db.execute(select(Profile).where(Profile.user_uuid == user_uuid))
    profile = profile.scalar_one_or_none()

    if profile is None:
        raise credentials_exception

    return profile