from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
from backend.crud import (
    create_task,
    get_task,
    get_all_tasks,
    update_task,
    delete_task
)


router = APIRouter()

@router.post("/task/", response_model=TaskResponse)
def create_task_route(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        return create_task(db=db, task=task)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal error in database: {e}"
        )
    
@router.get("/task/", response_model=List[TaskResponse])
def read_all_tasks_route(db: Session = Depends(get_db)):
    tasks = get_all_tasks(db)
    return tasks

@router.get("/task/{task_id}", response_model=TaskResponse)
def read_task_route(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/task/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    try:
        db_task = update_task(db, task_id=task_id, task=task)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal error in database: {e}"
        )

@router.delete("/task/{task_id}", response_model=TaskResponse)
def delete_task_route(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
