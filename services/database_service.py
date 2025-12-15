from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
import os
from dotenv import load_dotenv

# --- FIX: Import from the correct file (etl_models) ---
from models.etl_models import NormalizedMarketData, Base

# Load environment variables
load_dotenv()

# 1. Setup Database Connection
# It reads from .env or uses a default local connection string
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@localhost/kasparro"  # Update 'password' if needed
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Ensure tables exist
# This creates the table if it's missing (fixes the "relation does not exist" error)
Base.metadata.create_all(bind=engine)

def bulk_upsert_normalized_data(session, data_list):
    """
    Inserts data, or updates existing rows if a conflict on the PrimaryKey occurs.
    The Primary Key is a composite of (source_record_id, source_name).
    """
    if not data_list:
        return

    # 3. Define the UPSERT statement
    # Prepare the INSERT statement
    insert_stmt = insert(NormalizedMarketData).values(data_list)
    
    # Define the ON CONFLICT behavior
    upsert_stmt = insert_stmt.on_conflict_do_update(
        # The specific columns that act as the unique constraint/ID
        index_elements=['source_record_id', 'source_name'],
        
        # The columns to update if that ID already exists
        set_=dict(
            current_price_usd=insert_stmt.excluded.current_price_usd,
            market_cap_usd=insert_stmt.excluded.market_cap_usd,
            volume_24h_usd=insert_stmt.excluded.volume_24h_usd,
            percent_change_24h=insert_stmt.excluded.percent_change_24h,
            last_updated_at=insert_stmt.excluded.last_updated_at,
            ingestion_timestamp=func.now() # Update the ingestion time
        )
    )
    
    # Execute and commit
    session.execute(upsert_stmt)
    session.commit()