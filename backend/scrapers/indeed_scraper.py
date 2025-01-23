from bs4 import Tag
from typing import Dict, Any, List, Optional
from .base import BaseJobScraper
import logging
import json

class IndeedScraper(BaseJobScraper):
    async def search_jobs(self, job_title: str, location: str) -> List[Dict[str, Any]]:
        url = self.config.url.format(job_title=job_title, location=location)
        html = await self.fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.select(self.config.selectors['job_card'])
        jobs = []
        
        for card in job_cards:
            try:
                job_data = await self.parse_job_card(card)
                if job_data:
                    jobs.append(job_data)
            except Exception as e:
                logging.error(f"Error parsing Indeed job: {str(e)}")
                continue
                
        return jobs

    async def parse_job_card(self, card: Tag) -> Optional[Dict[str, Any]]:
        try:
            title = self.clean_text(card.select_one(self.config.selectors['title']).text)
            company = self.clean_text(card.select_one(self.config.selectors['company']).text)
            location = self.clean_text(card.select_one(self.config.selectors['location']).text)
            
            url = card.find('a', {'class': 'jcs-JobTitle'})['href']
            if not url.startswith('http'):
                url = f"https://www.indeed.com{url}"
            
            salary_elem = card.select_one(self.config.selectors['salary'])
            salary = self.clean_text(salary_elem.text) if salary_elem else None
            
            # Get full job description
            job_details = await self.fetch_job_details(url)
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "url": url,
                "description": job_details.get('description', ''),
                "requirements": job_details.get('requirements', []),
                "benefits": job_details.get('benefits', []),
                "source": "Indeed",
                "is_remote": "remote" in location.lower() or "remote" in title.lower()
            }
        except Exception as e:
            logging.error(f"Error parsing Indeed job card: {str(e)}")
            return None

    async def fetch_job_details(self, url: str) -> Dict[str, Any]:
        html = await self.fetch_page(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        description = soup.find('div', {'id': 'jobDescriptionText'})
        description_text = self.clean_text(description.text) if description else ""
        
        # Extract requirements and benefits
        requirements = []
        benefits = []
        
        requirements_section = soup.find(string=lambda text: text and 'requirements' in text.lower())
        if requirements_section:
            req_list = requirements_section.find_next('ul')
            if req_list:
                requirements = [self.clean_text(li.text) for li in req_list.find_all('li')]
        
        benefits_section = soup.find(string=lambda text: text and 'benefits' in text.lower())
        if benefits_section:
            ben_list = benefits_section.find_next('ul')
            if ben_list:
                benefits = [self.clean_text(li.text) for li in ben_list.find_all('li')]
        
        return {
            "description": description_text,
            "requirements": requirements,
            "benefits": benefits
        }
