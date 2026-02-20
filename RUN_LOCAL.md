# Run Locally - Quick Start

## Backend

```bash
cd backend
./run_local.sh
```

Or manually:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Server runs on: http://localhost:8000

## Frontend

**In a new terminal:**

```bash
cd frontend
./run_local.sh
```

Or manually:
```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

App runs on: http://localhost:8501

## Test Backend

```bash
cd backend
python3 test_api.py
```

Or manually:
```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is LangGraph?"}'
```

## Notes

- Backend works without Langfuse (optional for local testing)
- If you have `.env` with API keys, it will use real OpenAI responses
- Without API keys, it returns mock data (still works for testing)

