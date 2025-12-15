import asyncio
import logging
import sys
import os

# 1. Setup path so Python can find 'services' and 'models' folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.crypto_service import fetch_coingecko_data, fetch_coinpaprika_data
from services.database_service import SessionLocal, bulk_upsert_normalized_data

# 2. Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def run_etl_pipeline():
    logger.info("--- Starting ETL Pipeline ---")
    
    try:
        # --- 1. EXTRACT ---
        logger.info("Fetching data from CoinGecko & CoinPaprika...")
        
        # Run fetchers in parallel
        results = await asyncio.gather(
            fetch_coingecko_data(),
            fetch_coinpaprika_data(),
            return_exceptions=True
        )
        
        all_data = []
        for res in results:
            if isinstance(res, list):
                all_data.extend(res)
            else:
                logger.error(f"Provider failed: {res}")

        if not all_data:
            logger.warning("No data received from any provider.")
            return

        logger.info(f"Extracted {len(all_data)} records total.")

        # --- 2. TRANSFORM ---
        # Convert Pydantic models to dictionaries for SQLAlchemy
        clean_data = []
        for item in all_data:
            if hasattr(item, 'dict'):
                clean_data.append(item.dict())
            elif isinstance(item, dict):
                clean_data.append(item)
            else:
                logger.warning(f"Skipping unknown data format: {type(item)}")

        # --- 3. LOAD ---
        logger.info("Saving to database (Upsert)...")
        db = SessionLocal()
        try:
            bulk_upsert_normalized_data(db, clean_data)
            logger.info("Data committed to database successfully.")
        except Exception as db_err:
            logger.error(f"Database Error: {db_err}")
            db.rollback()
        finally:
            db.close()

        logger.info("--- ETL Pipeline Finished ---")

    except Exception as e:
        logger.error(f"Critical ETL Failure: {e}", exc_info=True)

if __name__ == "__main__":
    # Windows-specific fix for asyncio loops
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(run_etl_pipeline())