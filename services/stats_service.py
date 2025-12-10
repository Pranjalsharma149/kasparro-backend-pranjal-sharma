# services/stats_service.py

from sqlalchemy.orm import Session
from typing import List, Dict
# Note: You may also need 'from datetime import datetime' if you use datetime.now() here

# ... any other imports (e.g., db.models)

def get_etl_summary(db: Session) -> List[Dict]:
    """
    Retrieves the summary statistics for the ETL pipeline.
    
    db: The SQLAlchemy session dependency.
    """
    
    # ------------------------------------------------------------------------
    # FIX: Updated TEMPORARY Mock Data (Add the missing fields)
    # ------------------------------------------------------------------------
    mock_data = [
        {
            "source_name": "CoinPaprika", 
            "last_successful_run": "2025-12-10T10:00:00Z", 
            "total_records_processed": 1500,
            # ADD THESE TWO MISSING FIELDS:
            "avg_run_duration_seconds": 35.5, # Mock duration
            "success_rate": 0.999 # Mock rate (99.9%)
        },
        # You might have another entry for CoinGecko if your original code had it
    ]
    
    # ------------------------------------------------------------------------
    
    # REMINDER: Replace this mock data with your actual SQLAlchemy query later.
    return mock_data