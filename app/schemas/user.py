from typing import Optional

from pydantic import BaseModel, EmailStr, constr
from uuid import UUID
from enum import Enum
from datetime import datetime, date


class UserRole(str, Enum):
    USER = "User"
    ADMIN = "Admin"
    MODERATOR = "Moderator"


class UserStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    BANNED = "Banned"


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE


class UserCreate(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=6)
    birthdate: Optional[date] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    profile_id: int
    user_uuid: UUID
    access_token: str
