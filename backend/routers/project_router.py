from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
from backend.crud import (
    create_project,
    get_project,
    get_all_projects,
    update_project,
    delete_project
)


router = APIRouter()

@router.post("/project/", response_model=ProjectResponse)
def create_project_route(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        return create_project(db=db, project=project)
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal error in database: {e}"
        )
    

@router.get("/project/", response_model=List[ProjectResponse])
def read_all_projects_route(db: Session = Depends(get_db)):
    projects = get_all_projects(db)
    return projects


@router.get("/project/{project_id}", response_model=ProjectResponse)
def read_project_route(project_id: int, db: Session = Depends(get_db)):
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/project/{project_id}", response_model=ProjectResponse)
def update_project_route(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    try:
        db_project = update_project(db, project_id=project_id, project=project)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project


    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal error in database: {e}"
        )        

@router.delete("/project/{project_id}", response_model=ProjectResponse)
def delete_project_route(project_id: int, db: Session = Depends(get_db)):
    db_project = delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
