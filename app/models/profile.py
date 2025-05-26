from sqlalchemy import Column, String, Integer, Text, ForeignKey, Date, TIMESTAMP, func
from app.core.database import Base
from sqlalchemy.orm import relationship


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    avatar = Column(String(255), nullable=True)
    birthdate = Column(Date, nullable=True)
    fcm_token = Column(String(255), nullable=True)
    user_uuid = Column(ForeignKey("user.uuid"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", backref="profile", uselist=False)
    articles = relationship("Article", back_populates="profile", cascade="all, delete-orphan")
