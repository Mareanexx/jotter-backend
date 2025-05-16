from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date, datetime


class ProfileBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    fcm_token: Optional[str] = None


class ProfileCreate(ProfileBase):
    user_uuid: UUID


class ProfileOut(ProfileBase):
    id: int
    avatar: str
    user_uuid: UUID
    created_at: datetime
