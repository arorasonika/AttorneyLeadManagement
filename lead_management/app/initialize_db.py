from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = "sqlite:///./test.db"

# Ensure the DATABASE_URL is set
if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL found in environment variables")

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Import all models and create tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized!")

if __name__ == "__main__":
    init_db()