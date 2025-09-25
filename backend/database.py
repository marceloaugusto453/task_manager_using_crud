from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://user:password@postgres/mydatabase"

engine = create_engine(DATABASE_URL,echo=True)
SessionLocal = sessionmaker(bing=engine,autoflush=False,autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()