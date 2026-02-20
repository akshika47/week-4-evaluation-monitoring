"""
Backend API - FastAPI + Research Assistant
Deploy this to Render.com

Setup:
1. Create backend/ directory
2. Copy this file as main.py
3. Create requirements.txt (see below)
4. Push to GitHub
5. Deploy on Render.com
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

# Make Langfuse optional for local testing (Python 3.14 compatibility issue)
LANGFUSE_AVAILABLE = False
try:
    import langfuse
    from langfuse.decorators import observe
    LANGFUSE_AVAILABLE = True
except (ImportError, Exception) as e:
    # Create a no-op decorator if Langfuse is not available
    def observe(func=None, **kwargs):
        if func is None:
            return lambda f: f
        return func

app = FastAPI()

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) if os.getenv("OPENAI_API_KEY") else None


class Query(BaseModel):
    message: str


@observe()
def research_assistant(query: str) -> str:
    """Research assistant - automatically traced by Langfuse (if available)."""
    if not llm:
        return "[Mock] Research summary about the query. This is a placeholder response."
    
    prompt = f"""You are a research assistant. Answer the following query concisely and accurately.

Query: {query}

Provide a clear, factual answer."""

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    return response.content


@app.post("/chat")
async def chat(query: Query):
    """API endpoint for chat."""
    response = research_assistant(query.message)
    return {"response": response}


@app.get("/health")
async def health():
    """Health check endpoint for Render."""
    return {"status": "ok", "service": "research-assistant-api"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Research Assistant API",
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)"
        }
    }


# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

