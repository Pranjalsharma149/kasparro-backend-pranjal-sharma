import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # --- Database Settings (Used by database.py and docker-compose.yml) ---
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "kasparro_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "secret")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "kasparro_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db") # 'db' is the service name in docker-compose
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    # Combined URL for SQLAlchemy
    DATABASE_URL: str = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # --- API Key (Used by ETL service) ---
    # The actual API key provided in the assignment (use a secure source like Docker secrets in a real system)
    EXTERNAL_API_KEY: str = os.getenv("EXTERNAL_API_KEY", "your_default_key_here") 
    
    # --- API Service Metadata ---
    API_LATENCY_MS: float = 20.0 # Mock value for GET /data metadata

settings = Settings()