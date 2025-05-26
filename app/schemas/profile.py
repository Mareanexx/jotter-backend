from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import date, datetime


class ProfileBase(BaseModel):
    username: str
    bio: Optional[str] = None
    birthdate: Optional[date] = None


class ProfileCreate(ProfileBase):
    user_uuid: UUID


class ProfileOut(ProfileBase):
    id: int
    email: EmailStr
    avatar: Optional[str]
    user_uuid: UUID
    created_at: datetime


class UpdateProfileRequest(BaseModel):
    id: int
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    birthdate: Optional[date] = None
