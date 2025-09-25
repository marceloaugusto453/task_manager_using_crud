from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class UserModel(Base):
    __tablename__ = "user_table"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_email = Column(String, index=True)
    area = Column(String, index=True)
    created_at = Column(DateTime(timezone=True),default=func.now(),index=True)

    task = relationship("TaskModel",back_populates='responsible')