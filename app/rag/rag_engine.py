# app/rag/rag_engine.py
"""
Core RAG Engine for Hyre AI PoC
- Loads documents from data/hyre_docs/
- Embeds using OpenAI (text-embedding-3-small)
- Stores in Pinecone vector store (index: hyre-docs)
- Builds LlamaIndex VectorStoreIndex
- Returns streaming query engine

Compatible with:
- llama-index==0.11.16
- llama-index-vector-stores-pinecone==0.2.3
- pinecone-client==5.0.1
"""

import os
from pathlib import Path
from typing import Optional

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.indices.base import BaseIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore

# CORRECT PINECONE v5+ API
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

# === CONFIGURATION ===
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data" / "hyre_docs"
PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "hyre-docs")
EMBED_MODEL_NAME: str = "text-embedding-3-small"
TOP_K: int = 3  # Number of retrieved chunks

# Validate required env vars
required_env = ["PINECONE_API_KEY", "OPENAI_API_KEY"]
missing = [var for var in required_env if not os.getenv(var)]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# === CREATE DATA DIRECTORY + SAMPLE DOCS (if missing) ===
DATA_DIR.mkdir(parents=True, exist_ok=True)

# === PINECONE CLIENT & INDEX (v5+) ===
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pc.Index(PINECONE_INDEX_NAME)   # pc.Index()

# === EMBEDDING MODEL ===
embed_model = OpenAIEmbedding(model=EMBED_MODEL_NAME)

# === VECTOR STORE ===
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

def build_rag_index() -> BaseIndex:
    print(f"Loading documents from: {DATA_DIR.resolve()}")
    documents = SimpleDirectoryReader(
        input_dir=DATA_DIR,
        required_exts=[".txt", ".pdf", ".docx", ".md"],
        recursive=True
    ).load_data()

    if not documents:
        raise ValueError(f"No documents found in {DATA_DIR}")

    print(f"Loaded {len(documents)} documents. Building index...")

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True,
        transformations=None
    )

    # FIXED: use len(index.docstore.docs) instead of index.index_struct.node_count
    node_count = len(index.docstore.docs)
    print(f"Index built successfully with {node_count} nodes.")
    return index


def get_query_engine(index: Optional[BaseIndex] = None) -> RetrieverQueryEngine:
    """
    Return a streaming query engine.
    Builds the index if none is supplied.
    """
    if index is None:
        print("No index supplied – building one now...")
        index = build_rag_index()

    print(f"Creating streaming query engine (top_k={TOP_K})...")
    return index.as_query_engine(
        similarity_top_k=TOP_K,
        streaming=True,
        embed_model=embed_model
    )


# === LOCAL TESTING ===
if __name__ == "__main__":
    try:
        index = build_rag_index()
        engine = get_query_engine(index)

        test_query = "What is Xavier's experience with high-availability systems?"
        print(f"\nQuery: {test_query}\nAnswer:")
        response = engine.query(test_query)
        response.print_response_stream()
        print("\n")
    except Exception as e:
        print(f"Test failed: {e}")