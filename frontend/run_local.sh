#!/bin/bash
# Script to run the frontend locally

echo "🚀 Starting Research Assistant Frontend..."
echo ""

# Check if .streamlit/secrets.toml exists
if [ ! -f .streamlit/secrets.toml ]; then
    echo "⚠️  No secrets.toml found. Creating..."
    mkdir -p .streamlit
    cat > .streamlit/secrets.toml << EOF
API_URL = "http://localhost:8000"
EOF
    echo "✅ Created .streamlit/secrets.toml"
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

# Start Streamlit
echo ""
echo "✅ Starting Streamlit on http://localhost:8501"
echo "   Make sure your backend is running on http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""
streamlit run app.py

