from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class JobSearch(Base):
    __tablename__ = "job_searches"
    
    id = Column(String, primary_key=True)
    job_title = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_remote = Column(Boolean, default=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_jobs_found = Column(Integer, default=0)
    
    jobs = relationship("Job", back_populates="search")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True)
    search_id = Column(String, ForeignKey('job_searches.id'))
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text)
    salary = Column(String)
    is_remote = Column(Boolean, default=False)
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    requirements = Column(JSON)
    technologies = Column(JSON)
    experience_level = Column(String)
    benefits = Column(JSON)
    date_posted = Column(DateTime)
    date_scraped = Column(DateTime, default=datetime.utcnow)
    
    search = relationship("JobSearch", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(String, primary_key=True)
    job_id = Column(String, ForeignKey('jobs.id'))
    tailored_resume = Column(Text, nullable=False)
    cover_letter = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    job = relationship("Job", back_populates="applications")
