from fastapi import FastAPI
from backend.database import engine
from backend.routers import user_router, project_router, task_router
from backend.models import project_model, task_model, user_model


project_model.Base.metadata.create_all(bind=engine)
task_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(user_router.router, prefix="/api", tags=["Users"])
app.include_router(project_router.router, prefix="/api", tags=["Projects"])
app.include_router(task_router.router, prefix="/api", tags=["Tasks"])
