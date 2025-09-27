from sqlalchemy.orm import Session
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

    '''
    db_user = UserModel(name=user.name, email=user.email, area=user.area)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[UserModel]:
    '''

    '''
    return db.query(UserModel).filter(UserModel.user_id == user_id).first()

def get_all_users(db: Session) -> List[UserModel]:
    '''

    '''

    return db.query(UserModel).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[UserModel]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True



# -------------------- PROJECTS -------------------- #
def create_project(db: Session, project: ProjectCreate) -> ProjectModel:
    db_project = ProjectModel(project_name=project.project_name, project_description=project.project_description)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int) -> Optional[ProjectModel]:
    return db.query(ProjectModel).filter(ProjectModel.project_id == project_id).first()


def get_all_projects(db: Session) -> List[ProjectModel]:
    return db.query(ProjectModel).all()


def update_project(db: Session, project_id: int, project_update: ProjectUpdate) -> Optional[ProjectModel]:
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    update_data = project_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    db_project = get_project(db, project_id)
    if not db_project:
        return False
    db.delete(db_project)
    db.commit()
    return True


# -------------------- TASKS -------------------- #
def create_task(db: Session, task: TaskCreate) -> TaskModel:
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
    return db.query(TaskModel).filter(TaskModel.task_id == task_id).first()


def get_all_tasks(db: Session) -> List[TaskModel]:
    return db.query(TaskModel).all()


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[TaskModel]:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True