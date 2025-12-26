from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

def build_index(texts: list[str]):
    embeddings = OpenAIEmbeddings()
    docs = [Document(page_content=t) for t in texts]
    db = FAISS.from_documents(docs, embeddings)
    return db

def query_index(db, query: str, k: int = 2):
    results = db.similarity_search(query, k=k)
    return [r.page_content for r in results]