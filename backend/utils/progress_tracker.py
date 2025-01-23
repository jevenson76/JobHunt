# backend/utils/progress_tracker.py
from typing import Dict, Any
from datetime import datetime

class ProgressTracker:
    def __init__(self, websocket_manager, search_id: str):
        self.websocket_manager = websocket_manager
        self.search_id = search_id
        self.start_time = datetime.now()
        self.total_jobs = 0
        self.processed_jobs = 0
        self.status = "initializing"

    async def update_progress(self, step: str, progress: int, details: Dict[str, Any] = None):
        message = {
            "type": "progress",
            "search_id": self.search_id,
            "step": step,
            "progress": progress,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
            "status": self.status
        }
        await self.websocket_manager.broadcast_to_search(self.search_id, message)

    async def start_job(self, total_jobs: int):
        self.total_jobs = total_jobs
        self.status = "in_progress"
        await self.update_progress("starting", 0, {"total_jobs": total_jobs})

    async def job_processed(self, job_details: Dict[str, Any]):
        self.processed_jobs += 1
        progress = int((self.processed_jobs / self.total_jobs) * 100)
        await self.update_progress("processing", progress, {
            "processed": self.processed_jobs,
            "total": self.total_jobs,
            "last_job": job_details
        })

    async def complete(self, results: list):
        self.status = "completed"
        duration = (datetime.now() - self.start_time).total_seconds()
        await self.update_progress("completed", 100, {
            "total_jobs_found": len(results),
            "duration_seconds": duration
        })

    async def error(self, error_message: str):
        self.status = "error"
        await self.update_progress("error", 0, {"error_message": error_message})
