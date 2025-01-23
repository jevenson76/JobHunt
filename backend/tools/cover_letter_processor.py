# backend/tools/cover_letter_processor.py
from crewai import Tool
import openai
import logging
from typing import Dict

class CoverLetterProcessorTool(Tool):
    def __init__(self):
        super().__init__(
            name="Cover Letter Generator",
            description="Generates customized cover letters"
        )

    async def generate_cover_letter(
        self,
        template: str,
        resume_content: str,
        job_title: str,
        company: str,
        job_description: str,
        required_skills: list,
        culture_indicators: list
    ) -> str:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Generate a professional cover letter that:
                        1. Uses the template as a base
                        2. Highlights relevant experience
                        3. Demonstrates cultural fit
                        4. Shows enthusiasm
                        5. Addresses requirements"""
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Template: {template}
                        Job: {job_title} at {company}
                        Description: {job_description}
                        Required Skills: {', '.join(required_skills)}
                        Culture Indicators: {', '.join(culture_indicators)}
                        Resume: {resume_content}
                        """
                    }
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error generating cover letter: {str(e)}")
            return template