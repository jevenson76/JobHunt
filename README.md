# Job Search Automation System

An automated job search and application system using CrewAI, FastAPI, and React.

## Features

- Multi-platform job scraping from 35+ job boards
- AI-powered resume tailoring for each application
- Customized cover letter generation
- Real-time application tracking
- Websocket-based progress updates
- Supabase integration for data persistence

## Tech Stack

### Backend
- FastAPI
- CrewAI
- OpenAI GPT-4
- SQLAlchemy
- Alembic
- BeautifulSoup4
- Supabase

### Frontend
- React/Next.js
- TailwindCSS
- Radix UI Components
- WebSocket Client

## Installation

### Backend Setup

```bash
# Clone repository
git clone https://github.com/jevenson76/JobHunt.git
cd JobHunt

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run migrations
alembic upgrade head
```

### Frontend Setup

```bash
cd frontend
npm install
```

## Configuration

1. Create `.env` file with required credentials:
   - OpenAI API key
   - Supabase URL and key
   - Database URL
   - API configuration

2. Set up Supabase:
   - Create new project
   - Run provided SQL migrations
   - Configure authentication

3. Optional: Configure job board preferences in `config/job_boards.py`

## Usage

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Access the application at `http://localhost:3000`

## API Documentation

- OpenAPI docs: `http://localhost:8000/docs`
- WebSocket endpoint: `ws://localhost:8000/ws/{connection_id}`

## Features in Detail

### Job Search
- Concurrent scraping from multiple job boards
- Automatic deduplication
- Content extraction and analysis
- Real-time progress tracking

### Resume Processing
- AI-powered skill matching
- Experience highlighting
- Keyword optimization
- ATS compatibility

### Cover Letter Generation
- Company research integration
- Custom templating
- Tone and style matching
- Requirement alignment

### Application Tracking
- Status monitoring
- Analytics and insights
- Export capabilities
- History management

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push branch (`git push origin feature/name`)
5. Open Pull Request

## License

MIT License - See LICENSE file for details

## Support

- GitHub Issues: [Project Issues](https://github.com/yourusername/job-search-automation/issues)
- Documentation: [Project Wiki](https://github.com/yourusername/job-search-automation/wiki)
"""
