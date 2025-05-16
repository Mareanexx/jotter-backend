from pydantic import BaseModel, EmailStr, constr
from uuid import UUID
from enum import Enum
from datetime import datetime


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
    email: EmailStr
    password: constr(min_length=6)


class UserOut(BaseModel):
    uuid: UUID
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    user_uuid: str
