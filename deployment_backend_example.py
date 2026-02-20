"""
Backend Deployment Example - FastAPI + Agent
Deploy this to Render.com
"""

from fastapi import FastAPI
from pydantic import BaseModel
from langfuse.decorators import observe

# Import your agent (adjust import path as needed)
# from research_assistant.agent import root_agent
# Or use a simple example:
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

app = FastAPI()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) if os.getenv("OPENAI_API_KEY") else None


class Query(BaseModel):
    message: str


@observe()
def research_assistant(query: str) -> str:
    """Simple research assistant - automatically traced by Langfuse."""
    if not llm:
        return "[Mock] Research summary about the query."
    
    prompt = f"""You are a research assistant. Answer the following query concisely.

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
    """Health check endpoint."""
    return {"status": "ok"}


# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

