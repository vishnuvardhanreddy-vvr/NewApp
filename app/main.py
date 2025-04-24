from fastapi import FastAPI
from app.scraper.route import scraper_router
from app.utils.logging_config import setup_logging

logger = setup_logging()

app = FastAPI(
    title="Scraper",
    version="0.0.1"
)

# Include router from agents.py
app.include_router(scraper_router, prefix="/api", tags=["Scraper"])
