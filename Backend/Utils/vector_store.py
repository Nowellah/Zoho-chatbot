from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

def get_embeddings():
    """Initialize embeddings with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")
    return OpenAIEmbeddings(openai_api_key=api_key)

def build_index(texts: list[str]):
    """Build a FAISS vector index from a list of text chunks."""
    embeddings = get_embeddings()
    docs = [Document(page_content=t) for t in texts if t.strip()]
    if not docs:
        raise ValueError("No valid text provided to build index.")
    db = FAISS.from_documents(docs, embeddings)
    return db

def query_index(db, query: str, k: int = 2):
    """Search the FAISS index for the most relevant text chunks."""
    results = db.similarity_search(query, k=k)
    return [r.page_content for r in results]

def save_index(db, path: str = "faiss_index"):
    """Save FAISS index to local disk."""
    db.save_local(path)

def load_index(path: str = "faiss_index"):
    """Load FAISS index from local disk."""
    embeddings = get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)