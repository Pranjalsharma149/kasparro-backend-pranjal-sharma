# main.py

# 1. IMPORT DOTENV
from dotenv import load_dotenv

# 2. LOAD ENVIRONMENT VARIABLES from the local .env file
# This must be done BEFORE the application loads code that relies on these variables (like core.db)
load_dotenv()

# Original FastAPI imports
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Kasparro Backend API")

@app.get("/")
def home():
    return {"message": "Kasparro Backend Running Successfully 🚀"}

app.include_router(router)