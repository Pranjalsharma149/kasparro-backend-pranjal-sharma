from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, func, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base

# Define the base class for declarative class definitions
Base = declarative_base()

# --- 1. ETL Checkpoint Model ---

class ETLCheckpoint(Base):
    """Tracks the last successful run for incremental ingestion."""
    __tablename__ = 'etl_checkpoints'
    
    source_name = Column(String, primary_key=True, comment="e.g., 'coingecko', 'coinpaprika', 'csv_data'")
    
    # Used for filtering the next API/CSV call
    last_successful_timestamp = Column(DateTime(timezone=True), nullable=True)
    
    last_run_status = Column(String, default="FAILURE", comment="'SUCCESS', 'FAILURE'")
    records_processed = Column(Integer, default=0)
    duration_ms = Column(Integer, default=0)
    
    # Metadata for /stats endpoint
    last_start_time = Column(DateTime(timezone=True), default=func.now())
    last_end_time = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return (f"<ETLCheckpoint(source='{self.source_name}', "
                f"last_timestamp='{self.last_successful_timestamp}')>")

# --- 2. Raw Data Models ---

class RawCoinGecko(Base):
    __tablename__ = 'raw_coingecko'
    
    # Use the combination of ID and the update time from the source as a composite primary key
    source_id = Column(String, nullable=False)
    timestamp_key = Column(DateTime(timezone=True), nullable=False)
    
    # Store the entire raw response as JSON/Text
    data_payload = Column(Text, nullable=False)
    ingestion_time = Column(DateTime(timezone=True), default=func.now())
    
    __table_args__ = (
        PrimaryKeyConstraint('source_id', 'timestamp_key'),
    )

    def __repr__(self):
        return (f"<RawCoinGecko(source_id='{self.source_id}', "
                f"timestamp='{self.timestamp_key}')>")


# --- 3. Normalized Data Model ---

class NormalizedMarketData(Base):
    __tablename__ = 'normalized_data'
    
    # Unique ID across all sources for P1.2 Idempotency
    source_record_id = Column(String, nullable=False) 
    source_name = Column(String, nullable=False)
    
    # Core Unified Fields
    symbol = Column(String(10), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    current_price_usd = Column(Float, nullable=False)
    market_cap_usd = Column(Float, nullable=False)
    volume_24h_usd = Column(Float)
    percent_change_24h = Column(Float)
    
    # Timestamps
    last_updated_at = Column(DateTime(timezone=True), nullable=True)
    ingestion_timestamp = Column(DateTime(timezone=True), default=func.now())
    
    __table_args__ = (
        # Enforce uniqueness across all sources to guarantee Idempotency (P1.2)
        PrimaryKeyConstraint('source_record_id', 'source_name'),
    )

    def __repr__(self):
        return (f"<NormalizedMarketData(symbol='{self.symbol}', "
                f"price={self.current_price_usd})>")