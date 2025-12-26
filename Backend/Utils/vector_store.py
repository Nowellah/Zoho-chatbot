from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.summarize import load_summarize_chain

# Load environment variables
load_dotenv()


def get_embeddings():
    """Initialize embeddings with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")
    return OpenAIEmbeddings(openai_api_key=api_key)


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    """Split text into smaller overlapping chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    return splitter.split_text(text)


def build_index(texts: list[str]):
    """Build a FAISS vector index from a list of text chunks."""
    embeddings = get_embeddings()
    docs = []
    for t in texts:
        chunks = chunk_text(t)
        docs.extend([Document(page_content=c) for c in chunks if c.strip()])
    if not docs:
        raise ValueError("No valid text provided to build index.")
    db = FAISS.from_documents(docs, embeddings)
    return db


def query_index(db, query: str, k: int = 3):
    """Search FAISS index, retrieve top-k chunks, and summarize them into a single answer."""
    results = db.similarity_search(query, k=k)
    if not results:
        return "No relevant info found."

    # Combine chunks
    combined_texts = [r.page_content for r in results]

    # Summarize using ChatOpenAI
    llm = ChatOpenAI(temperature=0)  # deterministic summarization
    chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run(combined_texts)

    return summary


def save_index(db, path: str = "faiss_index"):
    """Save FAISS index to local disk."""
    db.save_local(path)


def load_index(path: str = "faiss_index"):
    """Load FAISS index from local disk."""
    embeddings = get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
