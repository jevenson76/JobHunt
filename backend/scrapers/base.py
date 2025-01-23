from bs4 import BeautifulSoup, Tag
import aiohttp
import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from config.job_boards import JobBoardConfig
from utils.rate_limiter import RateLimiter

class BaseJobScraper:
    def __init__(self, config: JobBoardConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.rate_limit)
        self.session: Optional[aiohttp.ClientSession] = None
        self.retry_count = 3
        self.retry_delay = 5

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.config.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, url: str) -> Optional[str]:
        for attempt in range(self.retry_count):
            try:
                async with self.rate_limiter:
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            return await response.text()
                        elif response.status == 429:  # Rate limited
                            await asyncio.sleep(self.retry_delay * (attempt + 1))
                            continue
            except Exception as e:
                logging.error(f"Error fetching {url}: {str(e)}")
                if attempt < self.retry_count - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
        return None

    async def search_jobs(self, job_title: str, location: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement search_jobs method")

    def clean_text(self, text: Optional[str]) -> str:
        if not text:
            return ""
        return " ".join(text.strip().split())
