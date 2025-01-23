# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uuid
import logging
from datetime import datetime
from typing import List

from config import settings
from database import get_db
from agents.crew_manager import JobSearchCrew
from utils.websocket_manager import WebsocketManager
from utils.progress_tracker import ProgressTracker
from schemas.search import SearchCreate, Search
from schemas.job import Job
from schemas.application import Application

app = FastAPI()
websocket_manager = WebsocketManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{connection_id}")
async def websocket_endpoint(websocket: WebSocket, connection_id: str):
    await websocket_manager.connect(websocket, connection_id)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket_manager.send_personal_message({"type": "pong"}, connection_id)
    except WebSocketDisconnect:
        websocket_manager.disconnect(connection_id)

@app.post("/api/search", response_model=Search)
async def start_job_search(request: SearchCreate, db: Session = Depends(get_db)):
    search_id = str(uuid.uuid4())
    connection_id = str(uuid.uuid4())
    
    search = Search(
        id=search_id,
        job_title=request.job_title,
        location=request.location,
        is_remote=request.is_remote,
        status="started",
        selected_boards=request.selected_boards,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        total_jobs_found=0
    )
    db.add(search)
    db.commit()

    progress_tracker = ProgressTracker(websocket_manager, search_id)
    websocket_manager.register_search(search_id, connection_id)

    crew = JobSearchCrew(
        job_boards=request.selected_boards,
        progress_tracker=progress_tracker,
        db_session=db
    )

    # Start search in background
    asyncio.create_task(crew.run_search(
        job_title=request.job_title,
        location=request.location,
        is_remote=request.is_remote,
        resume_content=request.resume_content,
        cover_letter_template=request.cover_letter_template,
        search_id=search_id
    ))

    return search

@app.get("/api/search/{search_id}", response_model=Search)
async def get_search_status(search_id: str, db: Session = Depends(get_db)):
    search = db.query(Search).filter(Search.id == search_id).first()
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    return search

@app.get("/api/search/{search_id}/jobs", response_model=List[Job])
async def get_search_jobs(
    search_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).filter(
        Job.search_id == search_id
    ).offset(skip).limit(limit).all()
    return jobs

@app.get("/api/job/{job_id}/applications", response_model=List[Application])
async def get_job_applications(job_id: str, db: Session = Depends(get_db)):
    applications = db.query(Application).filter(
        Application.job_id == job_id
    ).all()
    return applications

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)