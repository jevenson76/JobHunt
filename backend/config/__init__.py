from .settings import Settings
from .job_boards import JobBoardConfig, JobBoardCategory, JOB_BOARDS_CONFIG

settings = Settings()

__all__ = ['settings', 'JobBoardConfig', 'JobBoardCategory', 'JOB_BOARDS_CONFIG']

