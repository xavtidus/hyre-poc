# app/rag/api.py
"""
FastAPI entry point for Hyre AI PoC
- /ask → RAG over internal docs
- /agent → LangChain ReAct agent (RAG + web search)
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

# === RAG IMPORTS ===
from .rag_engine import build_rag_index, get_query_engine

# === AGENT ROUTER IMPORT ===
from app.agents.api import router as agent_router  # <-- Fixed: correct path

# === FASTAPI APP ===
app = FastAPI(
    title="Hyre AI PoC API",
    description="RAG + Agentic Workflows with LlamaIndex + LangChain",
    version="0.2.0"
)

# Global query engine
query_engine = None

# === RAG REQUEST MODEL ===
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)

# === STARTUP: BUILD RAG INDEX ===
@app.on_event("startup")
async def startup_event():
    global query_engine
    try:
        print("Building RAG index from data/hyre_docs...")
        index = build_rag_index()
        query_engine = get_query_engine(index)
        print("RAG engine initialized and ready for queries.")
    except Exception as e:
        print(f"Failed to initialize RAG engine: {e}")
        raise

# === HEALTH CHECK ===
@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "rag_engine": "ready" if query_engine else "initializing",
        "endpoints": ["/ask", "/agent", "/test"]
    }

# === RAG /ask ENDPOINT ===
@app.post("/ask", tags=["rag"])
async def ask_question(request: QueryRequest) -> StreamingResponse:
    if not query_engine:
        raise HTTPException(status_code=503, detail="RAG engine not ready")

    try:
        response = query_engine.query(request.question)

        async def token_stream() -> AsyncGenerator[str, None]:
            for token in response.response_gen:
                yield token
            yield "\n"

        return StreamingResponse(token_stream(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# === MOUNT AGENT ROUTER ===
app.include_router(agent_router)  # <-- This makes /agent work

# === LOCAL TEST PAGE ===
@app.get("/test")
async def test_page():
    return """
    <h2>Hyre AI PoC Test</h2>
    <h3>RAG (/ask)</h3>
    <textarea id="rag_q" rows="2" cols="60"></textarea><br>
    <button onclick="ask_rag()">Ask RAG</button>
    <pre id="rag_out"></pre>

    <h3>Agent (/agent)</h3>
    <textarea id="agent_q" rows="2" cols="60"></textarea><br>
    <button onclick="ask_agent()">Ask Agent</button>
    <pre id="agent_out"></pre>

    <script>
    async function ask_rag() {
        const q = document.getElementById('rag_q').value;
        const res = await fetch('/ask', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({question: q})});
        const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
        const out = document.getElementById('rag_out');
        out.textContent = '';
        while (true) { const {value, done} = await reader.read(); if (done) break; out.textContent += value; }
    }
    async function ask_agent() {
        const q = document.getElementById('agent_q').value;
        const res = await fetch('/agent', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({question: q})});
        const data = await res.json();
        document.getElementById('agent_out').textContent = JSON.stringify(data, null, 2);
    }
    </script>
    """