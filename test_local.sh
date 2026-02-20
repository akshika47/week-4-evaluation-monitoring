#!/bin/bash
# Test script to run both backend and frontend locally

echo "🧪 Testing Research Assistant Locally"
echo "======================================"
echo ""

# Test Backend
echo "📦 Testing Backend..."
cd backend

# Create venv if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt > /dev/null 2>&1

# Copy .env if available
if [ -f ../../week-3/.env ] && [ ! -f .env ]; then
    cp ../../week-3/.env .env
    echo "✅ Copied .env from week-3"
fi

# Start backend in background
echo "Starting backend server..."
python3 main.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for server to start
sleep 5

# Test health endpoint
echo ""
echo "Testing /health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✅ Backend is running!"
    echo "   Response: $HEALTH_RESPONSE"
else
    echo "❌ Backend failed to start"
    echo "   Check /tmp/backend.log for errors"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Test chat endpoint
echo ""
echo "Testing /chat endpoint..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "What is LangGraph?"}')

if [ $? -eq 0 ]; then
    echo "✅ Chat endpoint working!"
    echo "   Response preview: $(echo $CHAT_RESPONSE | head -c 100)..."
else
    echo "❌ Chat endpoint failed"
fi

echo ""
echo "======================================"
echo "✅ Backend is running on http://localhost:8000"
echo ""
echo "To test the frontend:"
echo "  1. Open a new terminal"
echo "  2. cd frontend"
echo "  3. ./run_local.sh"
echo ""
echo "Or run: cd frontend && streamlit run app.py"
echo ""
echo "Press Ctrl+C to stop the backend"
echo ""

# Keep running until interrupted
wait $BACKEND_PID

