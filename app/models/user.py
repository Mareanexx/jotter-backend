from sqlalchemy import Column, String, Enum as SqlEnum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.core.database import Base
import enum


class UserStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    BANNED = "Banned"


class UserRole(str, enum.Enum):
    USER = "User"
    ADMIN = "Admin"
    MODERATOR = "Moderator"


class User(Base):
    __tablename__ = "user"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    role = Column(String(10), nullable=False, default=UserRole.USER.value)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(10), nullable=False, default=UserStatus.ACTIVE.value)
    created_at = Column(TIMESTAMP, nullable=False)
