from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

# --- Core Imports ---
from services.database_service import SessionLocal
from services.crypto_service import get_market_data, get_etl_stats_service
from models.etl_models import PaginatedResponseSchema, ETLCheckpointSchema

# --- NEW Health Imports ---
from services.health_service import get_health_status 
from schemas.health import HealthResponse # <-- Imports the new schema

app = FastAPI(title="Kasparro Backend", version="1.0")

# Dependency: Get Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Kasparro API is running. Go to /docs for Swagger UI."}

# =========================================================
# 1. Market Data Endpoint
# =========================================================
@app.get(
    "/market-data",
    response_model=PaginatedResponseSchema, 
    response_model_exclude_none=True
)
def read_market_data(
    limit: int = Query(default=10, ge=1, le=100), 
    offset: int = Query(default=0, ge=0), 
    symbol: Optional[str] = Query(default=None, max_length=10), 
    db: Session = Depends(get_db)
):
    """ Fetch paginated and filtered market data from the PostgreSQL database. """
    try:
        data, total_count = get_market_data(db, limit=limit, offset=offset, symbol=symbol)
        
        return {
            "metadata": {
                "total": total_count,
                "limit": limit,
                "offset": offset
            },
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# =========================================================
# 2. ETL Stats Endpoint
# =========================================================
@app.get(
    "/stats",
    response_model=List[ETLCheckpointSchema],
    response_model_exclude_none=True
)
def read_etl_stats(
    db: Session = Depends(get_db)
):
    """ Get the status and last run details for the ETL process from the ETLCheckpoint table. """
    try:
        stats = get_etl_stats_service(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# =========================================================
# 3. Health Check Endpoint (NEW)
# =========================================================
@app.get(
    "/health",
    response_model=HealthResponse, # <-- Now works with the new schema
    response_model_exclude_none=True
)
def read_health_status(
    db: Session = Depends(get_db)
):
    """ Provides a comprehensive health check for the API, database, and ETL pipeline. """
    # Uses the new service function
    return get_health_status(db)