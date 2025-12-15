from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List, Tuple
from fastapi import HTTPException
import httpx 
import logging
from datetime import datetime

# --- CRITICAL IMPORTS ---
from models.etl_models import NormalizedMarketData, ETLCheckpoint # DB Models

logger = logging.getLogger(__name__)

# --- Configuration for ETL (External API URLs) ---
COINPAPRIKA_API_URL = "https://api.coinpaprika.com/v1/tickers" 
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"

# =========================================================
# 1. Internal Data Service (Reads from DB for API)
# =========================================================
def get_market_data(db: Session, limit: int, offset: int, symbol: Optional[str]) -> Tuple[List[NormalizedMarketData], int]:
    """
    Retrieves paginated and filtered market data directly from PostgreSQL.
    Used by your FastAPI endpoint (/market-data).
    """
    
    # 1. Build the Query
    query = db.query(NormalizedMarketData)

    # 2. Apply Filter 
    if symbol:
        # Filter for the symbol (case-insensitive)
        query = query.filter(NormalizedMarketData.symbol.ilike(f"%{symbol}%"))

    # 3. Get Total Count (Required for pagination metadata)
    total_count = query.count()

    # 4. Fetch the Data
    # Sort by Market Cap (descending) 
    data_list = query.order_by(desc(NormalizedMarketData.market_cap_usd)) \
                      .offset(offset) \
                      .limit(limit) \
                      .all()
    
    return data_list, total_count


# =========================================================
# 2. ETL Stats Service (Reads from DB for /stats API)
# =========================================================
def get_etl_stats_service(db: Session) -> List[ETLCheckpoint]:
    """
    Retrieves the run status records from the ETLCheckpoint table.
    Used by your FastAPI endpoint (/stats).
    """
    # Query all records from the ETLCheckpoint table
    stats = db.query(ETLCheckpoint).all()
    
    return stats


# =========================================================
# 3. CoinPaprika Service (Async Fetch + Normalize - Used by ETL script)
# =========================================================
async def fetch_coinpaprika_data() -> List[dict]:
    """
    Asynchronously fetches and NORMALIZES data from CoinPaprika.
    """
    # ... (Keep the rest of your original CoinPaprika fetch/normalize logic here) ...
    params = {"limit": 10}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(COINPAPRIKA_API_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            normalized_data = []
            for coin in data:
                normalized_data.append({
                    "source_record_id": coin["id"],
                    "source_name": "coinpaprika",
                    "symbol": coin["symbol"].upper(),
                    "name": coin["name"],
                    "current_price_usd": coin.get("quotes", {}).get("USD", {}).get("price", 0),
                    "market_cap_usd": coin.get("quotes", {}).get("USD", {}).get("market_cap", 0),
                    "volume_24h_usd": coin.get("quotes", {}).get("USD", {}).get("volume_24h", 0),
                    "percent_change_24h": coin.get("quotes", {}).get("USD", {}).get("percent_change_24h", 0),
                    "last_updated_at": coin["last_updated"]
                })
            return normalized_data

        except Exception as e:
            logger.error(f"Error fetching CoinPaprika data: {e}")
            return []

# =========================================================
# 4. CoinGecko Service (Async Fetch + Normalize - Used by ETL script)
# =========================================================
async def fetch_coingecko_data() -> List[dict]:
    """
    Asynchronously fetches and NORMALIZES data from CoinGecko.
    """
    # ... (Keep the rest of your original CoinGecko fetch/normalize logic here) ...
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(COINGECKO_API_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            normalized_data = []
            for coin in data:
                normalized_data.append({
                    "source_record_id": coin["id"],
                    "source_name": "coingecko",
                    "symbol": coin["symbol"].upper(),
                    "name": coin["name"],
                    "current_price_usd": coin["current_price"],
                    "market_cap_usd": coin["market_cap"],
                    "volume_24h_usd": coin["total_volume"],
                    "percent_change_24h": coin["price_change_percentage_24h"],
                    "last_updated_at": coin["last_updated"]
                })
            return normalized_data
            
        except Exception as e:
            logger.error(f"Error fetching CoinGecko data: {e}")
            return []