from fastapi import FastAPI, UploadFile, File
from typing import List
import shutil
from contextlib import asynccontextmanager

from Backend.Utils.file_dispatcher import dispatch_file
from Backend.Utils.vector_store import build_index, query_index, save_index, load_index
from Backend.Models.chat import ChatRequest, ChatResponse

app = FastAPI()
db = None  # global vector store

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db
    try:
        db = load_index()
        print("FAISS index loaded successfully.")
    except Exception:
        print("No existing index found. Starting fresh.")
    yield
    # Optional: add cleanup logic here if needed (e.g., closing DB connections)

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
    save_index(db)  # persist index

    return {"status": f"{len(files)} files ingested and saved successfully"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    global db
    if db is None:
        return ChatResponse(answer="Knowledge base is empty. Please upload files first.", routed_to="Human")

    answer = query_index(db, request.query, k=3)
    if answer.strip() and answer != "No relevant info found.":
        return ChatResponse(answer=answer, routed_to="AI")
    return ChatResponse(answer="No relevant info found. Routed to human.", routed_to="Human")