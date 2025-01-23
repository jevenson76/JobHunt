from crewai import Agent
from typing import List, Dict
from config.job_boards import JobBoardConfig
from scrapers.base import BaseJobScraper

class ScraperAgent(Agent):
    def __init__(self, config: JobBoardConfig):
        super().__init__(
            name=f"{config.name} Scraper",
            goal=f"Scrape job listings from {config.name}",
            backstory=f"Expert at extracting job data from {config.name}",
            verbose=True
        )
        self.config = config
        self.scraper = self._get_scraper_class()(config)

    def _get_scraper_class(self) -> type:
        scraper_name = self.config.name.lower().replace(' ', '')
        try:
            module = __import__(f'scrapers.{scraper_name}_scraper', fromlist=[''])
            return getattr(module, f'{self.config.name}Scraper')
        except ImportError:
            return BaseJobScraper

    async def execute(self, job_title: str, location: str) -> List[Dict]:
        async with self.scraper as scraper:
            return await scraper.search_jobs(job_title, location)
