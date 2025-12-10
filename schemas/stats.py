# schemas/stats.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StatsResponse(BaseModel):
    """Schema for individual ETL run summaries (as required by the /stats endpoint)."""
    source_name: str
    last_successful_run: Optional[datetime] = None
    last_failed_run: Optional[datetime] = None
    total_records_processed: int
    avg_run_duration_seconds: float
    success_rate: float # 0.0 to 1.0

# Note: If your /stats endpoint returns a *list* of these, 
# then the import `from schemas.stats import StatsResponse` is correct.