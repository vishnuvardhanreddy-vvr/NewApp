
import os
import logging
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import httpx
from app.agents.scraper_agent import get_data



async def get_markdown(url, removable_tags=[]):
    if not removable_tags:
        removable_tags = [
        'script', 'style', 'header', 'footer', 'nav', 'aside', 'select', 'head',
        'site-header', 'site-footer', 'main-nav', 'sidebar'
    ]
    html = await fetch_html(url=url)

    # Parse and clean HTML
    soup = BeautifulSoup(html, "html.parser")
    for tag in removable_tags:
        for element in soup.find_all(tag):
            element.decompose()  # Completely remove the tag and its contents

    cleaned_html = str(soup)
    markdown = md(cleaned_html)
    return markdown
    
    
async def fetch_html(url: str) -> str:
    timeout = httpx.Timeout(300.0)  # 5 minutes in seconds
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
    

async def get_scraped_data(url: str, removable_tags: list, use_ai: bool):
    result = {"scraped_text":"","scraped_json":{}}
    markdown = await get_markdown(url=url, removable_tags=removable_tags)
    if markdown:
        result['scraped_text'] = markdown
    if use_ai:
        result["scraped_json"] = await get_data()
    return result
