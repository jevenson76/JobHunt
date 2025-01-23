# backend/tasks/analyze_jobs_task.py
from crewai import Task
from typing import List, Dict
from utils.progress_tracker import ProgressTracker

class AnalyzeJobsTask(Task):
    def __init__(self, agent, jobs: List[Dict], progress_tracker: ProgressTracker):
        super().__init__(
            description=f"""
            Analyze {len(jobs)} job postings:
            1. Extract key requirements and skills
            2. Identify experience levels
            3. Parse compensation details
            4. Calculate match scores
            5. Remove duplicates
            """,
            agent=agent,
            context={"jobs": jobs},
            expected_output="List of analyzed job postings",
            async_execution=True
        )
        self.jobs = jobs
        self.progress_tracker = progress_tracker

    async def execute(self) -> List[Dict]:
        await self.progress_tracker.update_progress("analyzing", 50)
        analyzed_jobs = await self.agent.execute(self.jobs)
        await self.progress_tracker.update_progress("analysis_complete", 75)
        return analyzed_jobs