from crewai import Crew, Task
from typing import List, Dict, Optional
import asyncio
import logging
from datetime import datetime
from config.job_boards import JOB_BOARDS_CONFIG
from agents.analyzers import JobAnalyzerAgent
from agents.processors import ResumeAgent, CoverLetterAgent
from agents.scrapers import ScraperAgent
from database.models import JobSearch, Job
from utils.progress_tracker import ProgressTracker
from schemas.job import JobCreate

class JobSearchCrew:
    def __init__(
        self,
        job_boards: List[str],
        progress_tracker: ProgressTracker,
        db_session = None
    ):
        self.job_boards = job_boards
        self.progress_tracker = progress_tracker
        self.db_session = db_session
        
        # Initialize agents
        self.scraper_agents = [
            ScraperAgent(JOB_BOARDS_CONFIG[board])
            for board in job_boards
            if board in JOB_BOARDS_CONFIG
        ]
        
        self.analyzer_agent = JobAnalyzerAgent()
        self.resume_agent = ResumeAgent()
        self.cover_letter_agent = CoverLetterAgent()
        
        # Initialize tasks list
        self.tasks = []

    def _create_scraping_tasks(self, job_title: str, location: str, is_remote: bool) -> List[Task]:
        tasks = []
        for agent in self.scraper_agents:
            task = Task(
                description=f"""
                Search for {job_title} positions on {agent.config.name}
                Location: {location if not is_remote else 'Remote'}
                Steps:
                1. Search jobs matching criteria
                2. Extract detailed information
                3. Validate and clean data
                4. Store results
                """,
                agent=agent,
                context={
                    "job_title": job_title,
                    "location": location,
                    "is_remote": is_remote
                }
            )
            tasks.append(task)
        return tasks

    def _create_analysis_task(self, jobs: List[Dict]) -> Task:
        return Task(
            description=f"""
            Analyze {len(jobs)} job postings:
            1. Extract key requirements and skills
            2. Identify required experience levels
            3. Parse compensation information
            4. Calculate match scores
            5. Remove duplicates
            """,
            agent=self.analyzer_agent,
            context={"jobs": jobs}
        )

    def _create_application_tasks(
        self,
        jobs: List[Dict],
        resume_content: str,
        cover_letter_template: str
    ) -> List[Task]:
        tasks = []
        for job in jobs:
            # Resume tailoring task
            tasks.append(Task(
                description=f"""
                Tailor resume for {job['title']} at {job['company']}:
                1. Analyze job requirements
                2. Highlight relevant experience
                3. Add key skills and keywords
                4. Format appropriately
                """,
                agent=self.resume_agent,
                context={
                    "job": job,
                    "resume_content": resume_content
                }
            ))
            
            # Cover letter generation task
            tasks.append(Task(
                description=f"""
                Generate cover letter for {job['title']} at {job['company']}:
                1. Use provided template
                2. Customize for company
                3. Highlight relevant experience
                4. Show enthusiasm and fit
                """,
                agent=self.cover_letter_agent,
                context={
                    "job": job,
                    "resume_content": resume_content,
                    "template": cover_letter_template
                }
            ))
        return tasks

    async def store_results(self, jobs: List[Dict], search_id: str):
        if not self.db_session:
            return
        
        try:
            for job_data in jobs:
                job = JobCreate(**job_data, search_id=search_id)
                db_job = Job(**job.dict())
                self.db_session.add(db_job)
            
            # Update search record
            search = self.db_session.query(JobSearch).filter_by(id=search_id).first()
            if search:
                search.total_jobs_found = len(jobs)
                search.status = "completed"
                search.updated_at = datetime.utcnow()
            
            await self.db_session.commit()
            
        except Exception as e:
            logging.error(f"Error storing results: {str(e)}")
            await self.db_session.rollback()
            raise

    async def run_search(
        self,
        job_title: str,
        location: str,
        is_remote: bool,
        resume_content: Optional[str] = None,
        cover_letter_template: Optional[str] = None,
        search_id: Optional[str] = None
    ):
        try:
            # Initialize progress
            total_steps = len(self.job_boards) + 1  # Scraping + analysis
            if resume_content and cover_letter_template:
                total_steps += 1  # Applications
            await self.progress_tracker.start_job(total_steps)

            # Create and execute scraping tasks
            scraping_tasks = self._create_scraping_tasks(job_title, location, is_remote)
            all_jobs = []
            
            for task in asyncio.as_completed(scraping_tasks):
                jobs = await task
                all_jobs.extend(jobs)
                await self.progress_tracker.job_processed({
                    "source": task.agent.config.name,
                    "jobs_found": len(jobs)
                })

            # Analyze jobs
            analysis_task = self._create_analysis_task(all_jobs)
            analyzed_jobs = await analysis_task.execute()
            
            # Generate applications if requested
            if resume_content and cover_letter_template:
                application_tasks = self._create_application_tasks(
                    analyzed_jobs,
                    resume_content,
                    cover_letter_template
                )
                final_results = await asyncio.gather(*application_tasks)
            else:
                final_results = analyzed_jobs

            # Store results
            if search_id and self.db_session:
                await self.store_results(final_results, search_id)

            await self.progress_tracker.complete(final_results)
            return final_results

        except Exception as e:
            logging.error(f"Error in job search: {str(e)}")
            await self.progress_tracker.error(str(e))
            raise

    def get_crew(self) -> Crew:
        return Crew(
            agents=[
                *self.scraper_agents,
                self.analyzer_agent,
                self.resume_agent,
                self.cover_letter_agent
            ],
            tasks=self.tasks,
            verbose=True
        )