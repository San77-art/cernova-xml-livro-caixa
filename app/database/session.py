from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Senha nova: NovaPassword123!@Segura
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:NovaPassword123!%40Segura@cernova-rb-db.c61cukey2jxy.us-east-1.rds.amazonaws.com:5432/cernova_rb")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()