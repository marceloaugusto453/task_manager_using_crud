from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base


class ProjectModel(Base):
    __tablename__ = "project_table"

    project_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    project_description = Column(String, index = True)
    created_at = Column(DateTime(timezone=True),default=func.now(),index=True)

    tasks = relationship("TaskModel", back_populates="project")