# frontend/src/pages/index.js
import JobSearchUI from '../components/JobSearchUI';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <JobSearchUI />
    </div>
  );
}

# frontend/package.json
{
  "name": "job-search-automation",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "@radix-ui/react-switch": "^1.0.0",
    "@radix-ui/react-tabs": "^1.0.0",
    "lucide-react": "^0.294.0",
    "next": "^14.0.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^3.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.9.0",
    "@types/react": "^18.2.37",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "typescript": "^5.2.2"
  }
}