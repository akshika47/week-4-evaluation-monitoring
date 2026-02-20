#!/bin/bash
# Script to run the backend locally

echo "🚀 Starting Research Assistant Backend..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please add your API keys!"
    else
        echo "❌ No .env.example found. Please create .env manually."
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Start server
echo ""
echo "✅ Starting server on http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""
python3 main.py

