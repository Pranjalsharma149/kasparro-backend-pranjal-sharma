from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import List, Optional, Tuple
import time

# Import your DB Model for the query
from models.etl_models import ETLCheckpoint 
# Import the schemas for type hinting
from schemas.health import HealthResponse, ETLStatus 

def check_db_connectivity(db: Session) -> Tuple[str, Optional[int]]:
    """Checks database connection and reports latency."""
    try:
        start_time = time.time()
        # Execute a simple query to test connection
        db.execute(text("SELECT 1"))
        db_latency_ms = int((time.time() - start_time) * 1000)
        return "Connected", db_latency_ms
    except Exception as e:
        return f"Failed: {str(e)}", None

def get_etl_checkpoints(db: Session) -> List[ETLStatus]:
    """
    Fetches the actual ETL run status from the database.
    """
    # Query all records from the ETLCheckpoint table
    db_stats = db.query(ETLCheckpoint).all()

    # Map the SQLAlchemy models to the Pydantic Schema (ETLStatus)
    etl_list = []
    for stat in db_stats:
        etl_list.append(
            ETLStatus(
                source_name=stat.source_name,
                last_run_timestamp=stat.last_end_time or datetime.min,
                last_run_status=stat.last_run_status,
                last_processed_records=stat.records_processed,
                # Simple check for 'up-to-date': last run was successful
                is_up_to_date=(stat.last_run_status == "SUCCESS") 
            )
        )
    return etl_list

def get_health_status(db: Session) -> HealthResponse:
    """
    The main function required by the API route.
    Gathers DB status and ETL checkpoints.
    """
    db_status, db_latency = check_db_connectivity(db)
    
    if db_status.startswith("Connected"):
        etl_list = get_etl_checkpoints(db)
        
        # Check if all ETLs were successful for overall system status
        overall_status = "OK" 
        for e in etl_list:
             if e.last_run_status != "SUCCESS":
                 overall_status = "Degraded"
                 break
        
    else:
        # If DB is down, we cannot check ETL status
        etl_list = []
        overall_status = "Critical"

    return HealthResponse(
        database_status=db_status,
        database_latency_ms=db_latency,
        etl_checkpoints=etl_list,
        system_status=overall_status
    )