from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from app.core.database import Base


class Report(Base):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
