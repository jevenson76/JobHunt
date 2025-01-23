# backend/tools/job_analyzer.py
from crewai import Tool
import openai
import logging
from typing import Dict

class JobAnalyzerTool(Tool):
    def __init__(self):
        super().__init__(
            name="Job Description Analyzer",
            description="Analyzes job postings for key information"
        )

    async def analyze_job_description(
        self,
        description: str,
        requirements: str = "",
        benefits: str = ""
    ) -> Dict:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Analyze the job posting and extract:
                        1. Required skills
                        2. Preferred skills
                        3. Experience level
                        4. Technology stack
                        5. Cultural indicators
                        Return as structured data."""
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Description: {description}
                        Requirements: {requirements}
                        Benefits: {benefits}
                        """
                    }
                ],
                temperature=0.2
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error analyzing job description: {str(e)}")
            return {}
