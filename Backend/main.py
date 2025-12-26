from fastapi import FastAPI, UploadFile, File
from typing import List
import shutil
from contextlib import asynccontextmanager

from Backend.Utils.file_dispatcher import dispatch_file
from Backend.Utils.vector_store import build_index, query_index, save_index, load_index
from Backend.Models.chat import ChatRequest, ChatResponse

# Simple FAQ dictionary
FAQS = {
    "office hours": "Our office is open Monday to Friday, 9 AM – 5 PM.",
    "contact": "You can reach us at support@example.com or call +256-700-123456.",
    "location": "We are located at Plot 12, Kampala Road, Kampala, Uganda.",
    "services": "We provide accounting, auditing, and tax advisory services.",
}
app = FastAPI()
db = None  # global vector store
CONFIDENCE_THRESHOLD = 0.65  # adjust as needed


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db
    try:
        db = load_index()
        print("FAISS index loaded successfully.")
    except Exception:
        print("No existing index found. Starting fresh.")
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/ingest")
async def ingest_files(files: List[UploadFile] = File(...)):
    texts = []
    for file in files:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = dispatch_file(file.filename)
        if text.strip():
            texts.append(text)

    global db
    db = build_index(texts)
    save_index(db)

    return {"status": f"{len(files)} files ingested and saved successfully"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    global db
    query = request.query.lower()

    # Step 1: Check FAQ dictionary
    for keyword, answer in FAQS.items():
        if keyword in query:
            return ChatResponse(answer=answer, routed_to="AI")

    # Step 2: Fall back to knowledge base
    if db is None:
        return ChatResponse(
            answer="Knowledge base is empty. Please upload files first.",
            routed_to="Human",
        )

    # Use similarity search with scores
    results = db.similarity_search_with_score(request.query, k=3)
    if not results:
        return ChatResponse(
            answer="No relevant info found. Routed to human.", routed_to="Human"
        )

    # Check confidence threshold
    best_chunk, score = results[0]
    if score >= CONFIDENCE_THRESHOLD:
        # Summarize top chunks
        answer = query_index(db, request.query, k=3)
        return ChatResponse(answer=answer, routed_to="AI")
    else:
        return ChatResponse(
            answer="Confidence too low. Routed to human.", routed_to="Human"
        )
