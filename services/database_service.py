from sqlalchemy.dialects.postgresql import insert
from models.normalized_models import NormalizedMarketData
# Assume session is a SQLAlchemy Session object

def bulk_upsert_normalized_data(session, data_list):
    """
    Inserts data, or updates existing rows if a conflict on the PrimaryKey occurs.
    """
    # 1. Prepare data for bulk insert
    # data_list is a list of dictionaries, where each dict matches the column names.
    
    # 2. Define the UPSERT statement
    insert_stmt = insert(NormalizedMarketData).values(data_list)
    
    # 3. Specify what to do ON CONFLICT
    # The conflict target is the table's PrimaryKey (__table_args__),
    # which is ('source_record_id', 'source_name').
    upsert_stmt = insert_stmt.on_conflict_do_update(
        # Specify the columns that define the conflict
        index_elements=['source_record_id', 'source_name'],
        
        # Specify the columns to update if a conflict is found
        # We use insert_stmt.excluded.<column_name> to get the value
        # from the *current* row being inserted.
        set_=dict(
            current_price_usd=insert_stmt.excluded.current_price_usd,
            market_cap_usd=insert_stmt.excluded.market_cap_usd,
            volume_24h_usd=insert_stmt.excluded.volume_24h_usd,
            percent_change_24h=insert_stmt.excluded.percent_change_24h,
            last_updated_at=insert_stmt.excluded.last_updated_at,
            ingestion_timestamp=func.now() # Update the ingestion time
        )
    )
    
    session.execute(upsert_stmt)
    session.commit()