# backend/schemas/application.py
from pydantic import BaseModel
from datetime import datetime

class ApplicationBase(BaseModel):
    job_id: str
    tailored_resume: str
    cover_letter: str

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
