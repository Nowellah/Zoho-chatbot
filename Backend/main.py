from fastapi import FastAPI, UploadFile, File
from typing import List
from Backend.Utils.file_dispatcher import dispatch_file
from Backend.Utils.vector_store import build_index, query_index
from Backend.Models.chat import ChatRequest, ChatResponse
import shutil

app = FastAPI()
db = None  # global vector store

@app.post("/ingest")
async def ingest_files(files: List[UploadFile] = File(...)):
    texts = []

    for file in files:
        # Save each uploaded file locally
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Dispatch to correct loader
        text = dispatch_file(file.filename)
        texts.append(text)

    # Build vector index from all ingested files
    global db
    db = build_index(texts)

    return {"status": f"{len(files)} files ingested successfully"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    global db
    if db is None:
        return ChatResponse(answer="Knowledge base is empty. Please upload files first.", routed_to="Human")

    answer = query_index(db, request.query, k=3)  # fetch top 3 chunks
    if answer.strip():
        return ChatResponse(answer=answer, routed_to="AI")
    return ChatResponse(answer="No relevant info found. Routed to human.", routed_to="Human")