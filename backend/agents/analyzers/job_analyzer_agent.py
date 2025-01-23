from crewai import Agent
from typing import List, Dict
from tools.job_analyzer import JobAnalyzerTool

class JobAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Job Requirements Analyzer",
            goal="Analyze job postings to extract key requirements and assess fit",
            backstory="""Expert at analyzing job descriptions to identify key 
            requirements, skills, and company culture indicators.""",
            verbose=True,
            tools=[JobAnalyzerTool()]
        )
        
    async def analyze_posting(self, job_data: Dict) -> Dict:
        """Analyze a single job posting."""
        analysis = await self.tools[0].analyze_job_description(
            job_data['description'],
            job_data.get('requirements', ''),
            job_data.get('benefits', '')
        )
        
        return {
            **job_data,
            'analysis': analysis,
            'skill_keywords': analysis['skills'],
            'experience_level': analysis['experience_level'],
            'required_skills': analysis['required_skills'],
            'preferred_skills': analysis['preferred_skills'],
            'culture_indicators': analysis['culture_indicators']
        }
    
    async def execute(self, jobs: List[Dict]) -> List[Dict]:
        """Analyze multiple job postings."""
        analyzed_jobs = []
        for job in jobs:
            analyzed = await self.analyze_posting(job)
            analyzed_jobs.append(analyzed)
        return analyzed_jobs
