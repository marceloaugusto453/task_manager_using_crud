from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
from enum import Enum
from backend.schemas.user_schema import UserResponse
from backend.schemas.project_schema import ProjectResponse


class StatusBase(str, Enum):
    to_do = "To-do"
    doing = "Doing"
    finished = "Finished"


class TaskBase(BaseModel):
    task_name: str
    task_description: str
    status: str
    deadline: datetime
    project_id: int
    user_id: int

    @validator("status")
    def check_status(cls, v):
        if v not in [item.value for item in StatusBase]:
            raise ValueError("This status doesn't exist. Please, try again")
        return v


class TaskCreate(TaskBase):
    pass 


class TaskResponse(TaskBase):
    task_id: int
    project: ProjectResponse
    responsible: UserResponse

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    task_description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
    project_id: Optional[int] = None
    user_id: Optional[int] = None
