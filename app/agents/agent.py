# app/agents/agent.py
"""
LangGraph ReAct-style Agent for Hyre AI PoC (LangChain 1.0+)
Tools:
- rag_search: Internal RAG (LlamaIndex)
- web_search: DuckDuckGo
"""

import os
from typing import Any
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# Import RAG query engine
from ..rag.rag_engine import get_query_engine

load_dotenv()

# === CONFIG ===
LLM_MODEL = "gpt-4o-mini"
TOP_K = 3

# === TOOLS ===
@tool
def rag_search(query: str) -> str:
    """Search internal Hyre documents, CV, and website PDFs."""
    engine = get_query_engine()
    response = engine.query(query)
    return "".join([token for token in response.response_gen])

@tool
def web_search(query: str) -> str:
    """Search the public web using DuckDuckGo."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

tools = [rag_search, web_search]

# === LLM ===
llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

# === SYSTEM PROMPT ===
system_prompt = (
    "You are Hyre's AI Architect Assistant. Use tools to answer questions.\n"
    "Tools available:\n"
    "- rag_search: Internal Hyre job PD, CV, website PDFs\n"
    "- web_search: Public internet\n\n"
    "Think step-by-step. Use tools when needed."
)

# === AGENT ===
agent_executor = create_react_agent(llm, tools, prompt=system_prompt)

def run_agent(question: str) -> str:
    """Run agent and return final answer."""
    result = agent_executor.invoke({"messages": [("user", question)]})
    # Get the last message from the agent
    last_message = result["messages"][-1]
    return last_message.content