from crewai import Agent
from typing import Dict
import openai
from tools.resume_processor import ResumeProcessorTool

class ResumeAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Resume Tailoring Specialist",
            goal="Customize resumes for specific job applications",
            backstory="""Expert at analyzing job requirements and tailoring 
            resumes to highlight relevant experience and skills.""",
            verbose=True,
            tools=[ResumeProcessorTool()]
        )
    
    async def execute(self, resume_content: str, job_data: Dict) -> str:
        """Tailor resume for a specific job."""
        analysis = job_data.get('analysis', {})
        
        return await self.tools[0].tailor_resume(
            resume_content=resume_content,
            job_requirements=analysis.get('required_skills', []),
            preferred_skills=analysis.get('preferred_skills', []),
            experience_level=analysis.get('experience_level', ''),
            job_description=job_data.get('description', '')
        )
