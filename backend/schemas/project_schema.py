from pydantic import BaseModel, validator, PositiveFloat, EmailStr, validator, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class ProjectBase(BaseModel):
    project_name: str
    project_description: str


class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    project_description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True