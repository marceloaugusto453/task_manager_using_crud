from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.database import Base

class TaskModel(Base):
    __tablename__ = "task_table"

    task_id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, index=True)
    task_description = Column(String, index=True)
    status = Column(String, index=True)
    deadline = Column(DateTime)

    project_id = Column(Integer, ForeignKey("project_table.project_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_table.user_id"),nullable=False)

    project = relationship("ProjectModel",back_populates='task_table')
    responsible = relationship("UserModel",back_populates='task_table')
