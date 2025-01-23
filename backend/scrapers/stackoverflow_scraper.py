# backend/scrapers/stackoverflow_scraper.py
from bs4 import Tag
from typing import Dict, Any, List, Optional
from .base import BaseJobScraper
import logging

class StackOverflowScraper(BaseJobScraper):
    async def search_jobs(self, job_title: str, location: str) -> List[Dict[str, Any]]:
        url = self.config.url.format(job_title=job_title, location=location)
        html = await self.fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select('div.js-result')
        return [job for card in job_cards if (job := await self.parse_job_card(card))]

    async def parse_job_card(self, card: Tag) -> Optional[Dict[str, Any]]:
        try:
            title = self.clean_text(card.select_one('h2.mb4 a').text)
            company = self.clean_text(card.select_one('h3.fc-black-700').text)
            location = self.clean_text(card.select_one('span.fc-black-500').text)
            technologies = [tag.text for tag in card.select('a.post-tag')]
            
            url = card.select_one('h2.mb4 a')['href']
            if not url.startswith('http'):
                url = f"https://stackoverflow.com{url}"
            
            details = await self.fetch_job_details(url)
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "url": url,
                "technologies": technologies,
                "description": details.get('description', ''),
                "requirements": details.get('requirements', []),
                "benefits": details.get('benefits', []),
                "source": "Stack Overflow",
                "is_remote": "remote" in location.lower() or "remote" in title.lower(),
                "salary": details.get('salary'),
                "visa_sponsor": details.get('visa_sponsor', False)
            }
        except Exception as e:
            logging.error(f"Error parsing Stack Overflow job: {str(e)}")
            return None

    async def fetch_job_details(self, url: str) -> Dict[str, Any]:
        html = await self.fetch_page(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        description = soup.select_one('div.job-description')
        benefits = soup.select_one('section.benefits-section')
        requirements = soup.select_one('section.requirements-section')
        salary = soup.select_one('span.-salary')
        visa = soup.select_one('span.-visa')
        
        return {
            "description": self.clean_text(description.text) if description else "",
            "benefits": [li.text.strip() for li in benefits.select('li')] if benefits else [],
            "requirements": [li.text.strip() for li in requirements.select('li')] if requirements else [],
            "salary": self.clean_text(salary.text) if salary else None,
            "visa_sponsor": bool(visa)
        }