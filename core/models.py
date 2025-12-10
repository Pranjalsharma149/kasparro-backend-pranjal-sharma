from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from core.database import Base

# --- P0.1 Model: RAW Data Storage ---
class RawData(Base):
    """
    Stores the original, untransformed data from each source. (P0.1 Requirement)
    Using JSON or String allows flexibility for different source formats.
    """
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, index=True, nullable=False) # e.g., 'CoinPaprika', 'CSV_Source_A'
    source_unique_id = Column(String, unique=True, index=True) # Unique ID from the source (for deduping/idempotency)
    raw_content = Column(JSON, nullable=False) # Use JSON for API responses, can be text/string for CSV lines
    ingestion_timestamp = Column(DateTime(timezone=True), server_default=func.now())

# --- P0.1/P0.2 Model: Normalized Market Data ---
class NormalizedMarketData(Base):
    """
    Stores the unified, clean, and validated data. (P0.1/P0.2 Requirement)
    This is what the GET /data endpoint will query.
    """
    __tablename__ = "normalized_market_data"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Core Asset Identifiers
    asset_id = Column(String, index=True, nullable=False) # Unified ID for the asset (e.g., Bitcoin)
    symbol = Column(String, index=True, nullable=False)    # e.g., BTC, ETH

    # Market Data
    price_usd = Column(Float, nullable=False)
    volume_24h = Column(Float, nullable=True)
    market_cap_usd = Column(Float, nullable=True)
    
    # Metadata for Auditing/Source Tracking
    source_name = Column(String, nullable=False) # Source that provided this record
    last_updated = Column(DateTime(timezone=True), nullable=False) # Timestamp from the source API/Data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint for Idempotency (P1.2) - prevents duplicate records for the same asset at the same time from the same source
    # We will enforce this via code using ON CONFLICT, but the index is good practice
    __table_args__ = (
        # A combined unique constraint is robust for idempotent upserts
        # Using source_name and last_updated is a good unique key for time-series data
        # UniqueConstraint('asset_id', 'last_updated', 'source_name', name='uc_asset_time_source'),
    )


# --- P1.2/P1.3 Model: ETL Checkpoint and Statistics ---
class ETLCheckpoint(Base):
    """
    Tracks run status and metrics for incremental ingestion and the /stats endpoint.
    (P1.2/P1.3 Requirement)
    """
    __tablename__ = "etl_checkpoint"

    # Source Name is the Primary Key for a single entry per source
    source_name = Column(String, primary_key=True, index=True) 

    # Status & Timing
    last_successful_run = Column(DateTime(timezone=True), nullable=True)
    last_failed_run = Column(DateTime(timezone=True), nullable=True)
    current_status = Column(String, default="IDLE") # e.g., IDLE, RUNNING, SUCCESS, FAILED
    last_run_duration_seconds = Column(Float, nullable=True)

    # Metrics (for /stats endpoint)
    total_records_processed = Column(Integer, default=0) # Total records processed by THIS source historically
    success_rate = Column(Float, default=1.0) # Calculated success rate
    
    # Failure/Resume Logic (P1.2)
    last_checkpoint_value = Column(String, nullable=True) # Used to store the 'last_updated' value to resume from
    failure_details = Column(String, nullable=True) # Store traceback/error message