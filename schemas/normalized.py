from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class MarketData(BaseModel):
    """
    Schema matches the 'normalized_data' table in database.
    """
    source_record_id: str
    source_name: str
    symbol: str
    name: str
    current_price_usd: float
    market_cap_usd: float
    volume_24h_usd: float
    percent_change_24h: float
    last_updated_at: Optional[datetime]

    # critical: allows pydantic to read sqlalchemy objects
    model_config = ConfigDict(from_attributes=True)

class PaginationMetadata(BaseModel):
    request_id: str
    api_latency_ms: int
    total_records: int
    limit: int
    offset: int
    filter_applied: Dict[str, Optional[Any]] = {}

class PaginatedResponse(BaseModel):
    """The final response structure for paginated data."""
    metadata: PaginationMetadata
    data: List[MarketData]