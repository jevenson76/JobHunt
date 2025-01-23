from enum import Enum
from typing import Dict, List
from pydantic import BaseModel

class JobBoardCategory(str, Enum):
    GENERAL = "general"
    TECH = "tech"
    REMOTE = "remote"
    FREELANCE = "freelance"
    STARTUP = "startup"

class JobBoardConfig(BaseModel):
    name: str
    url: str
    category: JobBoardCategory
    requires_auth: bool = False
    api_available: bool = False
    rate_limit: int = 60
    selectors: Dict[str, str] = {}
    headers: Dict[str, str] = {}

JOB_BOARDS_CONFIG = {
    "indeed": JobBoardConfig(
        name="Indeed",
        url="https://www.indeed.com/jobs?q={job_title}&l={location}",
        category=JobBoardCategory.GENERAL,
        selectors={
            "job_card": "div.job_seen_beacon",
            "title": "h2.jobTitle",
            "company": "span.companyName",
            "location": "div.companyLocation",
            "salary": "span.salary-snippet",
            "description": "div.job-snippet"
        }
    ),
    "linkedin": JobBoardConfig(
        name="LinkedIn",
        url="https://www.linkedin.com/jobs/search?keywords={job_title}&location={location}",
        category=JobBoardCategory.GENERAL,
        requires_auth=True,
        selectors={
            "job_card": "div.base-card",
            "title": "h3.base-search-card__title",
            "company": "h4.base-search-card__subtitle",
            "location": "span.job-search-card__location"
        }
    ),
    # Add more job boards...
}
