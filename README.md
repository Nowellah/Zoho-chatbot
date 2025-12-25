# Zoho AI-Enhanced Sales & Support Platform

## 📌 Overview
This project is a Python-based backend service that integrates with **Zoho CRM, Zoho Desk, and Zoho SalesIQ** to deliver an AI-enhanced customer engagement and digital sales platform.  
It automates customer support, manages leads and workflows, and provides intelligent query handling through a chatbot connected to a knowledge base.

The system is designed to:
- Fetch and manage leads from Zoho CRM.
- Automate ticket routing in Zoho Desk.
- Handle customer queries via Zoho SalesIQ with AI-powered responses.
- Search a **knowledge base** of documents, videos, and images to provide context-aware answers.
- Route complex queries to human agents when necessary.

---

## 🏗️ Architecture
- **Backend Service**: Python + FastAPI (REST API endpoints).
- **Integrations**: Zoho CRM, Zoho Desk, Zoho SalesIQ APIs.
- **Chatbot Engine**:
  - Rule-based FAQ handling.
  - Intent detection (ML/NLP-ready).
  - Knowledge base search (vector embeddings).
- **Knowledge Base**:
  - File storage for documents, videos, and images.
  - Indexing pipeline for text extraction and embeddings.
- **Routing Logic**:
  - AI answers simple queries.
  - Escalates complex queries to human agents.

---

## 📂 Project Structure
zoho-chatbot/ │ 
├── backend/              # Core backend services 
│── services/         # Zoho API clients, chatbot logic 
│─ models/           # Data models, schemas │   
└── utils/            # Helpers, config, logging │ 
├── knowledge_base/       # Stored files for chatbot reference │   
├── docs/             # PDFs, Word docs │   
├── videos/           # Transcripts, metadata │   
└── images/           # Captions, metadata │ 
├── tests/                # Unit and integration tests 
├── requirements.txt      # Python dependencies 
└── README.md             # Project documentation


---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Virtual environment (`venv` or `poetry`)
- Zoho API credentials (CRM, Desk, SalesIQ)

### Installation
```bash
git clone https://github.com/nowellah/zoho-chatbot.git
cd zoho-chatbot
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt

### Runing The Service
uvicorn backend.main:app --reload