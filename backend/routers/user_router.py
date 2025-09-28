from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from typing import List
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from backend.crud import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user
)

router = APIRouter()

@router.post("/user/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db=db, user=user)
    
    except IntegrityError as e:
        db.rollback()
        detail = "Error creating the user"

        if "null value in column" in str(e):
            detail = "You forgot to fill 1 or more fields"

        raise HTTPException(
            status_code=400,
            detail=detail
        )
    
    except SQLAlchemyError as e:        
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Internal error in database: {e}" 
        )

@router.get("/user/", response_model=List[UserResponse])
def read_all_users_route(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@router.get("/user/{user_id}", response_model=UserResponse)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/user/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        db_user = update_user(db, user_id=user_id, user=user)
        
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return db_user
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal error in database: {e}"
        )
        
    

@router.delete("/user/{user_id}", response_model=UserResponse)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
