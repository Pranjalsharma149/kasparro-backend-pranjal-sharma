# schemas/raw.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- CoinPaprika Example Structure ---
class CoinPaprikaCoin(BaseModel):
    id: str
    name: str
    symbol: str
    rank: int
    is_new: bool
    type: str

# CoinPaprika data often comes as a list of dictionaries at the top level
class CoinPaprikaResponse(CoinPaprikaCoin):
    """Placeholder for a single CoinPaprika coin object."""
    pass


# --- CoinGecko Example Structure ---
class CoinGeckoMarketData(BaseModel):
    current_price: float
    market_cap: int
    total_volume: int
    price_change_percentage_24h: float

class CoinGeckoCoin(BaseModel):
    id: str
    symbol: str
    name: str
    image: Optional[str] = None
    market_data: CoinGeckoMarketData

# CoinGecko market endpoint often returns a list of dictionaries
class CoinGeckoResponse(BaseModel):
    """Placeholder for a single CoinGecko item from the /markets endpoint."""
    id: str
    symbol: str
    name: str
    current_price: float
    market_cap: int
    total_volume: float
    # ... include other relevant fields from the API response