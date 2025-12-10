# services/health_service.py

from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import List, Optional # <-- FIX: Added 'Optional' here
import time

# Assuming you have the schemas defined above and corrected 'schemas/health.py'
from schemas.health import HealthResponse, ETLStatus

def check_db_connectivity(db: Session) -> tuple[str, Optional[int]]:
    """Checks database connection and reports latency."""
    try:
        start_time = time.time()
        # Execute a simple query (e.g., SELECT 1)
        db.execute(text("SELECT 1"))
        db_latency_ms = int((time.time() - start_time) * 1000)
        return "Connected", db_latency_ms
    except Exception as e:
        # In a real app, log the full error
        return f"Failed: {str(e)}", None

def get_etl_checkpoints(db: Session) -> List[ETLStatus]:
    """
    Simulated function to fetch ETL status.
    In a real app, this would query a table (e.g., 'etl_checkpoints')
    """
    # Placeholder implementation:
    current_time = datetime.now()
    
    # You would typically query a model like this:
    # return db.query(ETLCheckpointModel).all()
    
    return [
        ETLStatus(
            source_name="CoinPaprika",
            last_run_timestamp=current_time,
            last_run_status="Success",
            last_processed_records=1500,
            is_up_to_date=True
        ),
        ETLStatus(
            source_name="CoinGecko",
            last_run_timestamp=current_time,
            last_run_status="Failure",
            last_processed_records=0,
            is_up_to_date=False
        ),
    ]

def get_health_status(db: Session) -> HealthResponse:
    """
    The main function required by the API route.
    Gathers DB status and ETL checkpoints.
    """
    db_status, db_latency = check_db_connectivity(db)
    
    if db_status.startswith("Connected"):
        etl_list = get_etl_checkpoints(db)
        # Check if all ETLs were successful
        overall_status = "OK" if all(e.last_run_status == "Success" for e in etl_list) else "Degraded"
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