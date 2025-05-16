from sqlalchemy import Column, String, Integer, Text, ForeignKey, Date, TIMESTAMP
from app.core.database import Base
from sqlalchemy.orm import relationship


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255))
    bio = Column(Text)
    avatar = Column(String(255), nullable=True)
    birthdate = Column(Date, nullable=True)
    gender = Column(String(8))
    fcm_token = Column(String(255), nullable=True)
    user_uuid = Column(ForeignKey("user.uuid"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    user = relationship("User", backref="profile", uselist=False)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
