from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.database import Base
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = "user_table"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    area = Column(String, index=True)
    created_at = Column(DateTime(timezone=True),default=func.now(),index=True)

    tasks = relationship("TaskModel",back_populates='responsible')