import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.scraper.scraper import get_scraped_data

scraper_router = APIRouter()

# Example schema
class Scraper(BaseModel):
    url : str
    removable_tags: Optional[list] = []
    use_ai: Optional[bool] = False

# Example route
@scraper_router.post("/scraper")
async def run_agent(scraper: Scraper):
    url = scraper.url
    removable_tags = scraper.removable_tags
    use_ai = scraper.use_ai
    try:
        if not url:
            raise HTTPException(status_code=400, detail="Missing input URL")
        result = await get_scraped_data(url=url, removable_tags=removable_tags, use_ai=use_ai)
    except Exception as e:
        logging.error(str(e))
        result = {"scraped_content":"", "error":str(e)}

    return {"status": "success", "result": result}
