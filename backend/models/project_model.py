from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class ProjectModel(Base):
    __tablename__ = "project_table"

    project_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    project_description = Column(String, index = True)
    created_at = Column(DateTime(timezone=True),default=func.now(),index=True)

    task = relationship("Task", back_populates="project_table")