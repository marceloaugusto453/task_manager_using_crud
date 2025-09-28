from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional
from backend.models.user_model import UserModel
from backend.models.project_model import ProjectModel
from backend.models.task_model import TaskModel
from backend.schemas.user_schema import UserCreate, UserUpdate
from backend.schemas.project_schema import ProjectCreate, ProjectUpdate
from backend.schemas.task_schema import TaskCreate, TaskUpdate


#--------------------------USER--------------------------#

def create_user(db: Session, user: UserCreate) -> UserModel:
    '''
    CRUD step to receive the command to create the user in the database
    '''
    db_user = UserModel(name=user.name, email=user.email, area=user.area)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[UserModel]:
    '''
    CRUD step to filter the user and receive a response
    '''
    return db.query(UserModel).filter(UserModel.user_id == user_id).first()

def get_all_users(db: Session) -> List[UserModel]:
    '''
    CRUD step to receive all registered users
    '''

    return db.query(UserModel).all()


def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[UserModel]:
    '''
    CRUD step to perform an update on the user
    '''
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    '''
    Delete a user given an id.
    '''
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user



# -------------------- PROJECTS -------------------- #
def create_project(db: Session, project: ProjectCreate) -> ProjectModel:
    '''
    CRUD step to receive the command to create the project in the database
    '''
    db_project = ProjectModel(project_name=project.project_name, project_description=project.project_description)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int) -> Optional[ProjectModel]:
    '''
    CRUD step to filter the project and receive a response
    '''
    return db.query(ProjectModel).filter(ProjectModel.project_id == project_id).first()


def get_all_projects(db: Session) -> List[ProjectModel]:
    '''
    CRUD step to receive all registered projects
    '''
    return db.query(ProjectModel).all()


def update_project(db: Session, project_id: int, project: ProjectUpdate) -> Optional[ProjectModel]:
    '''
    CRUD step to perform an update on the project
    '''
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    '''
    Delete a project given an id.
    '''
    db_project = db.query(ProjectModel).filter(ProjectModel.project_id == project_id).first()
    db.delete(db_project)
    db.commit()
    return db_project


# -------------------- TASKS -------------------- #
def create_task(db: Session, task: TaskCreate) -> TaskModel:
    '''
    CRUD step to receive the command to create the task in the database
    '''
    db_task = TaskModel(
        task_name=task.task_name,
        task_description=task.task_description,
        status=task.status,
        deadline=task.deadline,
        project_id=task.project_id,
        user_id=task.user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Optional[TaskModel]:
    '''
    CRUD step to filter the task and receive a response
    '''
    return db.query(TaskModel).filter(TaskModel.task_id == task_id).first()


def get_all_tasks(db: Session) -> List[TaskModel]:
    '''
    CRUD step to receive all registered tasks
    '''
    return db.query(TaskModel).all()


def update_task(db: Session, task_id: int, task: TaskUpdate) -> Optional[TaskModel]:
    '''
    CRUD step to perform an update on the task
    '''
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> Optional[TaskModel]:
    '''
    Delete a task given an id. Error handled of not being able to return json.
    '''
    db_task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
    
    if db_task is None:
        return None
    
    task_data_to_return = db_task.__dict__.copy() 

    try:
        db.delete(db_task)
        db.commit()
        
        # Retorne o dicionário serializado
        return task_data_to_return 
        
    except Exception as e:
        db.rollback() 
        raise e 