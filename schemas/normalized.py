# schemas/normalized.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# Assuming your actual market data objects are defined somewhere else, 
# for now, we'll use a placeholder or define a simple one.
# If you have a CoinMarketData model, replace 'BaseModel' below with it.
class MarketData(BaseModel):
    # This should match the structure of your normalized database model/result
    asset_id: Optional[str] = None
    symbol: str
    price_usd: float
    last_updated: datetime
    # ... add other fields as necessary (e.g., volume, market_cap)
    pass 

class PaginationMetadata(BaseModel):
    request_id: str
    api_latency_ms: int
    total_records: int
    limit: int
    offset: int
    filter_applied: Dict[str, Optional[Any]] = {} # Dictionary to hold filters (e.g., symbol)

class PaginatedResponse(BaseModel):
    """The final response structure for paginated data."""
    metadata: PaginationMetadata
    data: List[MarketData]