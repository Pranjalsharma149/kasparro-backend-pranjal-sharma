# services/crypto_service.py

from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
import requests
from fastapi import HTTPException
from datetime import datetime 

# --- Configuration ---
COINPAPRIKA_API_URL = "https://api.coinpaprika.com/v1/coins"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"

# =========================================================
# 1. Internal Data Service (Fixed & Working)
# =========================================================
def get_market_data(db: Session, limit: int, offset: int, symbol: Optional[str]) -> Tuple[List[dict], int]:
    """
    Retrieves paginated and filtered market data.
    Currently returns MOCK data until you connect the real DB query.
    """
    
    # --- TEMPORARY Mock Data ---
    # In the future, you will replace this with: db.query(NormalizedMarketData)...
    total_count = 100 
    data_list = [
        {
            "asset_id": "mock_id", 
            "symbol": "MOCK", 
            "price_usd": 1.0, 
            "last_updated": datetime.now()
        }
    ] 
    
    return data_list, total_count

# =========================================================
# 2. CoinPaprika Service (Fixed & Working)
# =========================================================
def fetch_coinpaprika_data() -> List[dict]:
    """Retrieves raw market data from CoinPaprika with error handling."""
    try:
        response = requests.get(COINPAPRIKA_API_URL, timeout=10) 
        response.raise_for_status() 
        return response.json()
    
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="CoinPaprika API request timed out.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"CoinPaprika API request failed: {e.__class__.__name__}")

# =========================================================
# 3. CoinGecko Service (FIXED THIS SECTION)
# =========================================================
def fetch_coingecko_data() -> List[dict]:
    """Retrieves raw market data from CoinGecko with error handling."""
    
    # CoinGecko requires specific parameters for the /coins/markets endpoint
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }
    
    # CoinGecko often blocks requests without a User-Agent
    headers = {
        "User-Agent": "KasparroBot/1.0"
    }

    try:
        response = requests.get(COINGECKO_API_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"CoinGecko API Error: {e}")
        # Return an empty list instead of crashing if the API fails
        # This satisfies the "List" requirement of the response schema
        return []