from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Loads environment variables from the .env file
load_dotenv()

# Get the environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Database connection URL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Check the connection URL
print(f"Connecting to database: {DATABASE_URL}")

# Creates the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for the models
Base = declarative_base()

# Function to get a session from the database
def get_db():
    """
    Generator function to provide a database session.

    - **Yields**:
        - A database session (SessionLocal instance).

    - **Usage**:
        - Use this function as a dependency in FastAPI endpoints to get a database session.
        - The session is automatically closed after the request is processed.

    Example:
    ```python
    def some_endpoint(db: Session = Depends(get_db)):
        # Use the database session
        db.query(...)
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
