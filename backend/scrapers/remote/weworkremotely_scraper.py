# backend/scrapers/remote/weworkremotely_scraper.py
from bs4 import Tag
from typing import Dict, Any, List, Optional
from ..base import BaseJobScraper
import logging

class WeWorkRemotelyScraper(BaseJobScraper):
    async def search_jobs(self, job_title: str, location: str = "") -> List[Dict[str, Any]]:
        url = self.config.url.format(job_title=job_title)
        html = await self.fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select('li.feature')
        return [job for card in job_cards if (job := await self.parse_job_card(card))]

    async def parse_job_card(self, card: Tag) -> Optional[Dict[str, Any]]:
        try:
            title = self.clean_text(card.select_one('span.title').text)
            company = self.clean_text(card.select_one('span.company').text)
            job_type = self.clean_text(card.select_one('span.job-type').text)
            regions = card.select_one('span.region')
            regions = [r.strip() for r in regions.text.split(',')] if regions else []
            
            url = card.select_one('a')['href']
            if not url.startswith('http'):
                url = f"https://weworkremotely.com{url}"
            
            details = await self.fetch_job_details(url)
            
            return {
                "title": title,
                "company": company,
                "location": "Remote",
                "regions": regions,
                "job_type": job_type,
                "url": url,
                "description": details.get('description', ''),
                "requirements": details.get('requirements', []),
                "benefits": details.get('benefits', []),
                "source": "WeWorkRemotely",
                "is_remote": True
            }
        except Exception as e:
            logging.error(f"Error parsing WWR job: {str(e)}")
            return None

    async def fetch_job_details(self, url: str) -> Dict[str, Any]:
        html = await self.fetch_page(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        listing = soup.select_one('div.listing-container')
        
        description = ""
        requirements = []
        benefits = []
        
        for section in listing.select('div.listing-section'):
            title = section.select_one('h2')
            title = title.text.lower() if title else ""
            content = section.select_one('div.content')
            
            if "requirements" in title:
                requirements = [li.text.strip() for li in content.select('li')]
            elif "benefits" in title:
                benefits = [li.text.strip() for li in content.select('li')]
            else:
                description += self.clean_text(content.text) + "\n\n"
        
        return {
            "description": description.strip(),
            "requirements": requirements,
            "benefits": benefits
        }
