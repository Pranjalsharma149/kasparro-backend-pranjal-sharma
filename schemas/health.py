# schemas/health.py

from pydantic import BaseModel
# ------------------------------------------------
from typing import Optional, List  # <-- ADDED 'List' here
# ------------------------------------------------
from datetime import datetime

# Schema for the ETL status of a single source (e.g., CoinGecko, CoinPaprika)
class ETLStatus(BaseModel):
    source_name: str
    last_run_timestamp: Optional[datetime]
    last_run_status: str
    last_processed_records: int
    is_up_to_date: bool

# Final response model for the /health endpoint
class HealthResponse(BaseModel):
    database_status: str
    database_latency_ms: Optional[int]
    etl_checkpoints: List[ETLStatus] # <-- Now defined!
    system_status: str = "OK"