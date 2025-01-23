## README.md

# Job Search Automation System

An automated job search and application system using CrewAI, FastAPI, and React.

## Features

- Multi-platform job scraping
- Resume tailoring
- Cover letter generation
- Application tracking
- Real-time progress updates

## Installation

### Backend Setup

cd backend
python -m venv venv
source venv/bin/activate 

# Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head


### Frontend Setup

cd frontend
npm install

## Configuration

- Create .env file from template
- Set up Supabase database
- Configure OpenAI API key

## Usage

### Start Backend

cd backend
uvicorn main:app --reload

### Start Frontend

cd frontend
npm run dev

Access the application at http://localhost:3000

## API Documentation

API documentation available at http://localhost:8000/docs

## Tests

cd backend
pytest
