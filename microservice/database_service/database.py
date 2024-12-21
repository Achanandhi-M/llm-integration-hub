from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Fetch the DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase")

# Create a database engine (removed connect_args for PostgreSQL)
engine = create_engine(DATABASE_URL)

# Create a base class for the models to inherit from
Base = declarative_base()

# Create a sessionmaker factory to get a session for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to provide a database session to FastAPI endpoints.
    This will be used for managing transactions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
