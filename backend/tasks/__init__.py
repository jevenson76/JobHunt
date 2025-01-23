# backend/tasks/__init__.py
from .analyze_jobs_task import AnalyzeJobsTask
from .generate_applications_task import GenerateApplicationsTask
from .scrape_jobs_task import ScrapeJobsTask

__all__ = ['AnalyzeJobsTask', 'GenerateApplicationsTask', 'ScrapeJobsTask']

