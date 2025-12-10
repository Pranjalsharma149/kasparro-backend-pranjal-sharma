from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# 1. Define your Database URL
# This URL is read from the DATABASE_URL environment variable set in docker-compose.yml
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

# --- Error Check (Good Practice) ---
if SQLALCHEMY_DATABASE_URL is None:
    # This block prevents the ArgumentError if the environment variable is not set.
    # We expect the application to crash later, but this gives a clearer error message.
    raise EnvironmentError(
        "DATABASE_URL environment variable is not set. Cannot connect to database."
    )
# -----------------------------------

# 2. Create the engine
# Set pool_pre_ping=True to handle dropped connections in a long-running service
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

# 3. Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class for your models
# All your SQLAlchemy models will inherit from this Base class
Base = declarative_base()

# 5. Define the Dependency function 'get_db'
# This function is used by FastAPI endpoints to inject a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()