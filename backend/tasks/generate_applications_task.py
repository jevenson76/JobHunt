# backend/tasks/generate_applications_task.py
from crewai import Task
from typing import List, Dict
from utils.progress_tracker import ProgressTracker

class GenerateApplicationsTask(Task):
    def __init__(
        self,
        agent,
        jobs: List[Dict],
        resume_content: str,
        cover_letter_template: str,
        progress_tracker: ProgressTracker
    ):
        super().__init__(
            description=f"""
            Generate applications for {len(jobs)} jobs:
            1. Tailor resume for each position
            2. Generate custom cover letters
            3. Create application packages
            4. Format documents
            5. Store results
            """,
            agent=agent,
            context={
                "jobs": jobs,
                "resume": resume_content,
                "template": cover_letter_template
            },
            expected_output="List of generated applications",
            async_execution=True
        )
        self.jobs = jobs
        self.resume_content = resume_content
        self.cover_letter_template = cover_letter_template
        self.progress_tracker = progress_tracker

    async def execute(self) -> List[Dict]:
        total_jobs = len(self.jobs)
        completed = 0

        applications = []
        for job in self.jobs:
            application = await self.agent.execute(
                resume_content=self.resume_content,
                cover_letter_template=self.cover_letter_template,
                job_data=job
            )
            applications.append(application)
            
            completed += 1
            progress = (completed / total_jobs) * 100
            await self.progress_tracker.update_progress("generating_applications", progress)

        return applications