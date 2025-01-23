from bs4 import Tag
from typing import Dict, Any, List, Optional
from .base import BaseJobScraper
import logging
import json

class LinkedInScraper(BaseJobScraper):
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
                logging.error(f"Error parsing LinkedIn job: {str(e)}")
                continue
                
        return jobs

    async def parse_job_card(self, card: Tag) -> Optional[Dict[str, Any]]:
        try:
            title = self.clean_text(card.select_one(self.config.selectors['title']).text)
            company = self.clean_text(card.select_one(self.config.selectors['company']).text)
            location = self.clean_text(card.select_one(self.config.selectors['location']).text)
            
            url = card.find('a', {'class': 'base-card__full-link'})['href']
            
            # Get job details
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
                "source": "LinkedIn",
                "is_remote": "remote" in location.lower() or "remote" in title.lower(),
                "experience_level": job_details.get('experience_level'),
                "employment_type": job_details.get('employment_type')
            }
        except Exception as e:
            logging.error(f"Error parsing LinkedIn job card: {str(e)}")
            return None

    async def fetch_job_details(self, url: str) -> Dict[str, Any]:
        html = await self.fetch_page(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try to get structured data first
        structured_data = None
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if data.get('@type') == 'JobPosting':
                    structured_data = data
                    break
            except:
                continue
        
        if structured_data:
            return {
                "description": structured_data.get('description', ''),
                "salary": structured_data.get('baseSalary', {}).get('value', {}).get('value'),
                "requirements": structured_data.get('skills', []),
                "benefits": structured_data.get('jobBenefits', []),
                "experience_level": structured_data.get('experienceRequirements'),
                "employment_type": structured_data.get('employmentType')
            }
        
        # Fallback to HTML parsing
        description = soup.select_one('div.show-more-less-html__markup')
        description_text = self.clean_text(description.text) if description else ""
        
        return {
            "description": description_text,
            "requirements": self.extract_requirements(soup),
            "benefits": self.extract_benefits(soup)
        }
