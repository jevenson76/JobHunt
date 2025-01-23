# backend/tasks/scrape_jobs_task.py
from crewai import Task
from typing import List, Dict
from utils.progress_tracker import ProgressTracker

class ScrapeJobsTask(Task):
    def __init__(
        self,
        agent,
        job_title: str,
        location: str,
        is_remote: bool,
        progress_tracker: ProgressTracker
    ):
        super().__init__(
            description=f"""
            Search for {job_title} positions:
            Location: {location if not is_remote else 'Remote'}
            Steps:
            1. Search multiple job boards
            2. Extract job details
            3. Validate data
            4. Remove duplicates
            """,
            agent=agent,
            context={
                "job_title": job_title,
                "location": location,
                "is_remote": is_remote
            },
            expected_output="List of job postings",
            async_execution=True
        )
        self.job_title = job_title
        self.location = location
        self.is_remote = is_remote
        self.progress_tracker = progress_tracker

    async def execute(self) -> List[Dict]:
        await self.progress_tracker.update_progress("scraping", 25)
        jobs = await self.agent.execute(
            self.job_title,
            self.location,
            self.is_remote
        )
        await self.progress_tracker.update_progress("scraping_complete", 50)
        return jobs