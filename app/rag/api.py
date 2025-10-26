# app/rag/api.py
"""
FastAPI wrapper for the Hyre RAG engine.
Provides a streaming /ask endpoint powered by LlamaIndex + Pinecone + OpenAI.

Features:
- Index built once at startup (idempotent)
- Streaming response via token stream
- Health check endpoint
- Pydantic validation
- Local HTML test page
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import AsyncGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import RAG engine (relative import)
from .rag_engine import build_rag_index, get_query_engine

# === FASTAPI APP ===
app = FastAPI(
    title="Hyre RAG API",
    description="Production-ready RAG service for Hyre AI PoC – LlamaIndex + Pinecone + OpenAI",
    version="0.1.0"
)

# Global query engine (initialized on startup)
query_engine = None


class QueryRequest(BaseModel):
    """Request model for /ask endpoint."""
    question: str = Field(..., min_length=1, max_length=1000, description="Question to ask the RAG system")


@app.on_event("startup")
async def startup_event():
    """Build or load the RAG index on startup (idempotent)."""
    global query_engine
    try:
        print("Building RAG index from data/hyre_docs...")
        index = build_rag_index()
        query_engine = get_query_engine(index)
        print("RAG engine initialized and ready for queries.")
    except Exception as e:
        print(f"Failed to initialize RAG engine: {e}")
        raise


@app.get("/", tags=["health"])
def health_check():
    """Simple health check."""
    return {
        "status": "healthy",
        "rag_engine": "ready" if query_engine else "initializing",
        "model": "text-embedding-3-small",
        "vector_store": "Pinecone (hyre-docs)"
    }


@app.post("/ask", tags=["query"])
async def ask_question(request: QueryRequest) -> StreamingResponse:
    """Stream response from the RAG engine."""
    if not query_engine:
        raise HTTPException(
            status_code=503,
            detail="RAG engine is not ready. Please try again in a few seconds."
        )

    try:
        response = query_engine.query(request.question)

        async def token_stream() -> AsyncGenerator[str, None]:
            for token in response.response_gen:
                yield token
            yield "\n"

        return StreamingResponse(token_stream(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


# === LOCAL TEST PAGE ===
@app.get("/test")
async def test_page():
    return """
    <h2>Hyre RAG API Test</h2>
    <textarea id="q" rows="3" cols="50" placeholder="Ask about Hyre or Xavier..."></textarea><br>
    <button onclick="ask()">Ask</button>
    <pre id="out"></pre>
    <script>
    async function ask() {
        const q = document.getElementById('q').value;
        const res = await fetch('/ask', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question: q})
        });
        const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
        const out = document.getElementById('out');
        out.textContent = '';
        while (true) {
            const {value, done} = await reader.read();
            if (done) break;
            out.textContent += value;
        }
    }
    </script>
    """