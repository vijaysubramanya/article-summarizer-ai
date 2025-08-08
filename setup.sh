#!/bin/bash

echo "Setting up Article Summarizer Web App..."

# Create virtual environment for backend
echo "Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate

# Start Django backend in background
echo "Starting Django backend server..."
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Go to frontend directory
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Start React frontend
echo "Starting React frontend server..."
npm start &
REACT_PID=$!

echo ""
echo "Article Summarizer is now running!"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo ""
echo "API Endpoints:"
echo "   - POST /api/summarize/ - Summarize article text"
echo "   - GET /api/health/ - Health check"
echo ""
echo "Model Location: models/checkpoint-1878/"
echo ""
echo "To stop the servers, press Ctrl+C"

# Wait for user to stop
wait 