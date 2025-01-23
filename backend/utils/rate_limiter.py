# backend/utils/rate_limiter.py
import asyncio
from datetime import datetime, timedelta
from collections import deque

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.rate = requests_per_minute
        self.window = 60  # seconds
        self.timestamps = deque()
        self._lock = asyncio.Lock()

    def __call__(self):
        return self

    async def __aenter__(self):
        async with self._lock:
            now = datetime.now()
            window_start = now - timedelta(seconds=self.window)
            
            while self.timestamps and self.timestamps[0] < window_start:
                self.timestamps.popleft()
            
            if len(self.timestamps) >= self.rate:
                wait_time = (self.timestamps[0] + timedelta(seconds=self.window) - now).total_seconds()
                await asyncio.sleep(max(0, wait_time))
            
            self.timestamps.append(now)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
