# ingestion/etl_main.py
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_etl_pipeline():
    logger.info("ETL pipeline started.")
    # Future P0.1/P1.1 Logic will go here
    time.sleep(2) 
    logger.info("ETL pipeline finished.")

if __name__ == "__main__":
    run_etl_pipeline()