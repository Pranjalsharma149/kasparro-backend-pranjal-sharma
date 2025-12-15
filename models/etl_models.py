from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, func, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional  # <-- CRITICAL: Optional is imported here

# Base class for SQLAlchemy models
Base = declarative_base()

# --- 1. ETL Checkpoint Model (Database Table) ---
class ETLCheckpoint(Base):
    __tablename__ = 'etl_checkpoints'
    
    source_name = Column(String, primary_key=True)
    last_successful_timestamp = Column(DateTime(timezone=True), nullable=True)
    last_run_status = Column(String, default="FAILURE")
    records_processed = Column(Integer, default=0)
    duration_ms = Column(Integer, default=0)
    last_start_time = Column(DateTime(timezone=True), default=func.now())
    last_end_time = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<ETLCheckpoint(source='{self.source_name}')>"

# --- 2. Raw Data Models (Database Tables - used by ETL ingestion) ---
class RawCoinGecko(Base):
    __tablename__ = 'raw_coingecko'
    source_id = Column(String, nullable=False)
    timestamp_key = Column(DateTime(timezone=True), nullable=False)
    data_payload = Column(Text, nullable=False)
    ingestion_time = Column(DateTime(timezone=True), default=func.now())
    __table_args__ = (PrimaryKeyConstraint('source_id', 'timestamp_key'),)

class RawCoinPaprika(Base):
    __tablename__ = 'raw_coinpaprika'
    source_id = Column(String, nullable=False)
    timestamp_key = Column(DateTime(timezone=True), nullable=False)
    data_payload = Column(Text, nullable=False)
    ingestion_time = Column(DateTime(timezone=True), default=func.now())
    __table_args__ = (PrimaryKeyConstraint('source_id', 'timestamp_key'),)

# --- 3. Normalized Data Model (Database Table - used by API) ---
class NormalizedMarketData(Base):
    __tablename__ = 'normalized_data'
    source_record_id = Column(String, nullable=False) 
    source_name = Column(String, nullable=False)
    symbol = Column(String(10), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    current_price_usd = Column(Float, nullable=False)
    market_cap_usd = Column(Float, nullable=False)
    volume_24h_usd = Column(Float)
    percent_change_24h = Column(Float)
    last_updated_at = Column(DateTime(timezone=True), nullable=True)
    ingestion_timestamp = Column(DateTime(timezone=True), default=func.now())
    __table_args__ = (PrimaryKeyConstraint('source_record_id', 'source_name'),)


# --- 4. Pydantic Schemas (For API Validation and Documentation) ---
class MarketDataSchema(BaseModel):
    """Schema for a single crypto market data record."""
    symbol: str
    name: str
    current_price_usd: float
    market_cap_usd: float
    volume_24h_usd: Optional[float] = None
    percent_change_24h: Optional[float] = None
    last_updated_at: Optional[datetime] = None
    source_name: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedResponseSchema(BaseModel):
    """Schema for the paginated /market-data response."""
    metadata: dict
    data: List[MarketDataSchema]

class ETLCheckpointSchema(BaseModel):
    """Schema for the /stats response."""
    source_name: str
    last_successful_timestamp: Optional[datetime]
    last_run_status: str
    records_processed: int
    duration_ms: int
    last_start_time: datetime
    last_end_time: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)