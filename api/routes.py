# api/routes.py - Corrected Version

from fastapi import APIRouter, Depends, Query, HTTPException, Request
from fastapi.encoders import jsonable_encoder # <--- ADDED: To ensure correct JSON encoding
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime # <--- ADDED: Used by datetime.now()
import uuid

# --- Core Dependencies ---
# Assuming 'core.db' contains the database connection logic and get_db function.
from core.db import get_db

# --- Service Imports ---
from services.crypto_service import get_market_data, fetch_coinpaprika_data, fetch_coingecko_data
from services.health_service import get_health_status 
from services.stats_service import get_etl_summary

# --- Schema Imports ---
from schemas.normalized import PaginatedResponse
from schemas.health import HealthResponse
from schemas.stats import StatsResponse
from schemas.raw import CoinPaprikaResponse, CoinGeckoResponse

# --- Router Initialization ---
router = APIRouter(prefix="/api", tags=["Kasparro API"])

# ==================================
# 1. RAW DATA ENDPOINTS
# ==================================

@router.get("/coinpaprika", response_model=List[CoinPaprikaResponse], summary="Fetches raw CoinPaprika data (Debug)")
def get_coinpaprika():
    """
    Retrieves raw market data directly from the CoinPaprika source (simulated or actual).
    """
    return fetch_coinpaprika_data()

@router.get("/coingecko", response_model=List[CoinGeckoResponse], summary="Fetches raw CoinGecko data (Debug)")
def get_coingecko():
    """
    Retrieves raw market data directly from the CoinGecko source (simulated or actual).
    """
    return fetch_coingecko_data()

# ==================================
# 2. MANDATORY BACKEND ENDPOINTS
# ==================================

@router.get(
    "/data", 
    response_model=PaginatedResponse, 
    summary="Paginated and Filtered Normalized Market Data"
)
def read_data(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page."),
    offset: int = Query(0, ge=0, description="Number of records to skip."),
    symbol: Optional[str] = Query(None, description="Filter by asset symbol (e.g., BTC, ETH)")
):
    """
    Retrieves normalized cryptocurrency market data from the database.
    Supports pagination and filtering by symbol. Returns request metadata.
    """
    start_time = datetime.now()
    request_id = str(uuid.uuid4())
    
    # 1. Fetch data from service layer
    # NOTE: The definition of get_market_data in services/crypto_service.py MUST be fixed!
    data_list, total_count = get_market_data(db, limit, offset, symbol)
    
    end_time = datetime.now()
    api_latency_ms = int((end_time - start_time).total_seconds() * 1000)

    # 2. Construct the required response structure
    response_content = {
        "metadata": {
            "request_id": request_id,
            "api_latency_ms": api_latency_ms,
            "total_records": total_count,
            "limit": limit,
            "offset": offset,
            "filter_applied": {"symbol": symbol}
        },
        "data": data_list
    }
    
    # Use jsonable_encoder for safety when dealing with complex types like datetime
    return jsonable_encoder(response_content)

@router.get(
    "/health", 
    response_model=HealthResponse, 
    summary="System Health Check (DB Connectivity, ETL Status)"
)
def get_health(db: Session = Depends(get_db)):
    """
    Reports connectivity to the database and the last run status of the ETL pipeline
    based on the 'etl_checkpoints' table.
    """
    # This calls the service function that combines DB check and ETL status lookup
    health_data = get_health_status(db)
    return health_data

# ==================================
# 3. MANDATORY GROWTH ENDPOINT
# ==================================

@router.get(
    "/stats", 
    response_model=List[StatsResponse], 
    summary="ETL Run Summaries"
)
def get_stats(db: Session = Depends(get_db)):
    """
    Exposes ETL summaries: records processed, duration, and last success/failure timestamps
    for all data sources tracked in the checkpoint table.
    """
    # This queries the database for ETL logs
    return get_etl_summary(db)

# ==================================
# 4. Simple Status Endpoint
# ==================================

@router.get("/status", summary="Simple Service Status Check")
def service_status():
    """Confirms the API application is running."""
    return {"service": "Kasparro Backend", "status": "Running"}