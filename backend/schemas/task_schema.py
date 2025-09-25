from pydantic import BaseModel, validator, PositiveFloat, EmailStr, validator, Field
from datetime import datetime
from typing import Optional
from enum import Enum
from backend.schemas.user_schema import UserResponse
from backend.schemas.project_schema import ProjectResponse

class StatusBase(Enum):
    status1 = "To-do"
    status2 = "Doing"
    status3 = "Finished"

class TaskBase(BaseModel):
    task_name: str
    task_description: str
    status = str
    deadline: datetime
    project_id: int
    user_id: int

    @validator("status"):
    def check_status(cls, v):
        if v in [item.value for item in StatusBase]:
            return v
        raise ValueError("This status doesn't exist. Please, try again")

class TaskCreate(TaskBase):
    project_id: int
    user_id: int

class TaskResponse(TaskBase):
    task_id: int
    project: ProjectResponse
    responsible: UserResponse

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    task_description: Optional[str] = None
    status = Optional[str] = None
    deadline: Optional[datetime] = None
    project_id: Optional[int] = None
    user_id: Optional[int] = None



task_id = Column(Integer, primary_key=True, index=True)
task_name = Column(String, index=True)
task_description = Column(String, index=True)
status = Column(String, index=True)
deadline = Column(DateTime)

    project_id = Column(Integer, ForeignKey("project_table.project_id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("user_table.user_id"),nullable=False)

    project = relationship("ProjectModel",back_populates='task_table')
    responsible = relationship("UserModel",back_populates='task_table')
