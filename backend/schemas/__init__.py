# backend/schemas/__init__.py
from .application import Application, ApplicationCreate
from .job import Job, JobCreate, JobUpdate
from .search import Search, SearchCreate, SearchUpdate

__all__ = ['Application', 'ApplicationCreate', 'Job', 'JobCreate', 'JobUpdate', 'Search', 'SearchCreate', 'SearchUpdate']
