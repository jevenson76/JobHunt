# backend/schemas/job.py
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
from datetime import datetime

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    url: HttpUrl
    description: Optional[str]
    salary: Optional[str]
    is_remote: bool
    source: str

class JobCreate(JobBase):
    search_id: str
    requirements: Optional[Dict]
    technologies: Optional[List[str]]
    experience_level: Optional[str]
    benefits: Optional[Dict]
    date_posted: Optional[datetime]

class JobUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    salary: Optional[str]
    requirements: Optional[Dict]
    technologies: Optional[List[str]]
    experience_level: Optional[str]
    benefits: Optional[Dict]

class Job(JobBase):
    id: str
    search_id: str
    requirements: Optional[Dict]
    technologies: Optional[List[str]]
    experience_level: Optional[str]
    benefits: Optional[Dict]
    date_posted: Optional[datetime]
    date_scraped: datetime

    class Config:
        orm_mode = True
