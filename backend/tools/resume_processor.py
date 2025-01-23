# backend/tools/resume_processor.py
from crewai import Tool
import openai
import logging

class ResumeProcessorTool(Tool):
    def __init__(self):
        super().__init__(
            name="Resume Tailor",
            description="Customizes resumes for specific jobs"
        )

    async def tailor_resume(
        self,
        resume_content: str,
        job_requirements: list,
        preferred_skills: list,
        experience_level: str,
        job_description: str
    ) -> str:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Tailor the resume to:
                        1. Match job requirements
                        2. Highlight relevant skills
                        3. Adjust experience descriptions
                        4. Add keywords
                        5. Maintain authenticity"""
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Resume: {resume_content}
                        Job Description: {job_description}
                        Required Skills: {', '.join(job_requirements)}
                        Preferred Skills: {', '.join(preferred_skills)}
                        Experience Level: {experience_level}
                        """
                    }
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error tailoring resume: {str(e)}")
            return resume_content