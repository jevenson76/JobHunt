rom crewai import Agent
from typing import Dict
import openai
from tools.cover_letter_processor import CoverLetterProcessorTool

class CoverLetterAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Cover Letter Writer",
            goal="Generate compelling, personalized cover letters",
            backstory="""Expert at crafting persuasive cover letters that 
            highlight relevant experience and demonstrate cultural fit.""",
            verbose=True,
            tools=[CoverLetterProcessorTool()]
        )
    
    async def execute(
        self, 
        template: str, 
        resume_content: str,
        job_data: Dict
    ) -> str:
        """Generate a customized cover letter."""
        analysis = job_data.get('analysis', {})
        
        return await self.tools[0].generate_cover_letter(
            template=template,
            resume_content=resume_content,
            job_title=job_data['title'],
            company=job_data['company'],
            job_description=job_data.get('description', ''),
            required_skills=analysis.get('required_skills', []),
            culture_indicators=analysis.get('culture_indicators', [])
        )