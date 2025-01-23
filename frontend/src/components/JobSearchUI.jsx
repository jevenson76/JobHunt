# frontend/src/components/JobSearchUI.jsx
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Search, Upload, MapPin, Briefcase } from 'lucide-react';

const JobSearchUI = () => {
  const [activeTab, setActiveTab] = useState('search');
  const [formData, setFormData] = useState({
    jobTitle: '',
    location: '',
    isRemoteOnly: false,
    resumeFile: null,
    coverLetterTemplate: '',
    selectedBoards: ['indeed', 'linkedin', 'glassdoor'],
    openaiKey: '',
    supabaseUrl: '',
    supabaseKey: ''
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [alert, setAlert] = useState(null);
  const [results, setResults] = useState([]);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (!ws) {
      const socket = new WebSocket('ws://localhost:8000/ws/connection1');
      setWs(socket);

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      };

      return () => {
        socket.close();
      };
    }
  }, []);

  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'progress':
        setAlert({
          type: 'info',
          message: data.message
        });
        break;
      case 'complete':
        setResults(data.results);
        setAlert({
          type: 'success',
          message: 'Job search completed!'
        });
        setActiveTab('results');
        break;
      case 'error':
        setAlert({
          type: 'error',
          message: data.message
        });
        break;
    }
  };

  const handleSubmit = async () => {
    setIsProcessing(true);
    setAlert(null);

    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      setAlert({
        type: 'info',
        message: 'Job search started...'
      });
    } catch (error) {
      setAlert({
        type: 'error',
        message: error.message
      });
      setIsProcessing(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="w-6 h-6" />
            Job Search Automation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            {/* Tabs implementation */}
            {/* Form fields implementation */}
            {/* Results display implementation */}
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default JobSearchUI;