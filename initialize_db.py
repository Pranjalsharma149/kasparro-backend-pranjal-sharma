# initialize_db.py

import sys
import time
from sqlalchemy.exc import OperationalError
from core.database import engine, Base
from core.models import RawData, NormalizedMarketData, ETLCheckpoint
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_RETRIES = 5
RETRY_DELAY = 5 # seconds

def init_db():
    logger.info("Attempting to connect to the database and create tables...")
    for i in range(MAX_RETRIES):
        try:
            # Create all tables defined in Base (RawData, NormalizedMarketData, ETLCheckpoint)
            Base.metadata.create_all(bind=engine)
            logger.info("Database connection successful and tables created.")
            return
        except OperationalError as e:
            logger.warning(f"Database connection failed (Attempt {i+1}/{MAX_RETRIES}). Retrying in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            sys.exit(1)

    logger.error("Failed to connect to the database after multiple retries. Exiting.")
    sys.exit(1)

if __name__ == "__main__":
    init_db()