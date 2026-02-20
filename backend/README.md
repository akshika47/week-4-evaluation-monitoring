# Backend API - Research Assistant

FastAPI backend for the Research Assistant. Deploy to Render.com.

## Setup

1. **Create a GitHub repository** for your backend
2. **Copy these files:**
   - `main.py` - FastAPI application
   - `requirements.txt` - Dependencies
   - `.env.example` - Environment variables template

3. **Set up environment variables:**
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `LANGFUSE_PUBLIC_KEY` - Your Langfuse public key
   - `LANGFUSE_SECRET_KEY` - Your Langfuse secret key
   - `LANGFUSE_HOST` - https://cloud.langfuse.com

## Deploy to Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** research-assistant-api (or your choice)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in the Render dashboard
6. Click "Create Web Service"
7. Wait for deployment (2-3 minutes)
8. Get your URL: `https://your-app.onrender.com`

## Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload

# Test the endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is LangGraph?"}'
```

## API Endpoints

- `POST /chat` - Send a query, get a response
- `GET /health` - Health check
- `GET /` - API information

