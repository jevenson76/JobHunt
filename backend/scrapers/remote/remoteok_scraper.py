# backend/scrapers/remote/remoteok_scraper.py
from bs4 import Tag
from typing import Dict, Any, List, Optional
from ..base import BaseJobScraper
import logging
import json

class RemoteOKScraper(BaseJobScraper):
    async def search_jobs(self, job_title: str, location: str = "") -> List[Dict[str, Any]]:
        url = self.config.url.format(job_title=job_title)
        html = await self.fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select('tr.job')
        return [job for card in job_cards if (job := await self.parse_job_card(card))]

    async def parse_job_card(self, card: Tag) -> Optional[Dict[str, Any]]:
        try:
            # RemoteOK stores job data in data-attributes
            job_data = json.loads(card['data-item'])
            
            technologies = [tag.text.strip() for tag in card.select('span.tag')]
            salary_elem = card.select_one('div.salary')
            
            return {
                "title": job_data['position'],
                "company": job_data['company'],
                "location": "Remote",
                "url": f"https://remoteok.io{job_data['url']}",
                "description": job_data.get('description', ''),
                "technologies": technologies,
                "salary": self.clean_text(salary_elem.text) if salary_elem else None,
                "source": "RemoteOK",
                "is_remote": True,
                "date_posted": job_data.get('date'),
                "company_logo": job_data.get('logo')
            }
        except Exception as e:
            logging.error(f"Error parsing RemoteOK job: {str(e)}")
            return None