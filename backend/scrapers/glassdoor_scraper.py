# backend/scrapers/glassdoor_scraper.py
from bs4 import Tag
from typing import Dict, Any, List, Optional
from .base import BaseJobScraper
import logging
import json

class GlassdoorScraper(BaseJobScraper):
    async def search_jobs(self, job_title: str, location: str) -> List[Dict[str, Any]]:
        url = self.config.url.format(job_title=job_title, location=location)
        html = await self.fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select('li.react-job-listing')
        jobs = []
        
        for card in job_cards:
            try:
                job_data = await self.parse_job_card(card)
                if job_data:
                    jobs.append(job_data)
            except Exception as e:
                logging.error(f"Error parsing Glassdoor job: {str(e)}")
                continue
                
        return jobs

    async def parse_job_card(self, card: Tag) -> Optional[Dict[str, Any]]:
        try:
            title = self.clean_text(card.select_one('a.jobLink').text)
            company = self.clean_text(card.select_one('div.emp-links').text)
            location = self.clean_text(card.select_one('span.loc').text)
            
            job_id = card.get('data-id')
            url = f"https://www.glassdoor.com/job-listing/job-listing.htm?id={job_id}"
            
            rating_elem = card.select_one('span.ratingsDisplay')
            company_rating = float(rating_elem.text) if rating_elem else None
            
            # Get full job details
            job_details = await self.fetch_job_details(url)
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "description": job_details.get('description', ''),
                "salary": job_details.get('salary'),
                "requirements": job_details.get('requirements', []),
                "benefits": job_details.get('benefits', []),
                "source": "Glassdoor",
                "is_remote": "remote" in location.lower() or "remote" in title.lower(),
                "company_rating": company_rating
