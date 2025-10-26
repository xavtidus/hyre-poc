# app/agents/api.py
"""
FastAPI endpoint for LangChain ReAct Agent
POST /agent → returns reasoning + final answer
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .agent import run_agent

router = APIRouter()

class AgentRequest(BaseModel):
    question: str

@router.post("/agent")
async def ask_agent(request: AgentRequest):
    """Run ReAct agent with RAG + web search."""
    try:
        answer = run_agent(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent failed: {str(e)}")