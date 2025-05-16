from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import TokenOut, UserLogin, UserOut, UserCreate
from app.core.database import get_db
from app.models.user import User, UserStatus
from passlib.hash import bcrypt
from app.core.security import create_access_token
from app.services.user import create_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenOut)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=403, detail="User is inactive or banned")

    token = create_access_token({"user_id": str(user.uuid)})
    return {"access_token": token, "user_uuid": str(user.uuid) }


@router.post("/register", response_model=UserOut)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(user_data, db)
