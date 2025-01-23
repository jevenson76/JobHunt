# backend/schemas/search.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SearchBase(BaseModel):
    job_title: str
    location: str
    is_remote: bool = False
    selected_boards: List[str]

class SearchCreate(SearchBase):
    resume_content: Optional[str]
    cover_letter_template: Optional[str]

class SearchUpdate(BaseModel):
    status: Optional[str]
    total_jobs_found: Optional[int]

class Search(SearchBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    total_jobs_found: int

    class Config:
        orm_mode = True