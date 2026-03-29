# RAG Document QA System

A document-grounded Retrieval-Augmented Generation (RAG) QA system built with **FastAPI**, **local embeddings**, and **Qdrant**.

This project demonstrates how to build an end-to-end RAG pipeline from scratch, including document ingestion, chunking, embedding, vector indexing, retrieval, and citation-aware answering.

---

## Features

- Upload local documents (`.txt`, `.pdf`)
- Extract document text
- Chunk long documents into overlapping segments
- Generate **local embeddings** using `sentence-transformers`
- Store embeddings and metadata in **Qdrant**
- Perform semantic search over documents
- Return answers grounded in retrieved content
- Provide **citation support** for transparency
- Interactive API testing via Swagger UI

---

## Tech Stack

- **Backend**: FastAPI
- **Vector Database**: Qdrant
- **Embedding Model**: `all-MiniLM-L6-v2`
- **PDF Parsing**: PyMuPDF
- **Language**: Python
- **Container Runtime**: Docker (for Qdrant)

---

## Pipeline

This project implements a basic Retrieval-Augmented Generation (RAG) pipeline:

1. Upload document  
2. Extract text from document  
3. Split text into chunks  
4. Generate embeddings for each chunk  
5. Store embeddings in Qdrant  
6. Embed user query  
7. Retrieve top-k relevant chunks  
8. Return answer with citation  

This pipeline enables document-grounded question answering with transparent citation support.

---

## Project Structure

```text
rag-document-qa/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── upload.py
│   │   ├── read.py
│   │   ├── chunk.py
│   │   ├── embed.py
│   │   ├── index.py
│   │   ├── query.py
│   │   └── answer.py
│   └── services/
│       ├── parser.py
│       ├── chunker.py
│       ├── embedder.py
│       └── vector_store.py
├── data/
│   └── uploads/
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example

## API Endpoints

### Basic
- `GET /`
- `GET /health`

### Document Processing
- `POST /upload`
- `POST /upload-and-read`
- `POST /upload-read-chunk`
- `POST /upload-read-chunk-embed`
- `POST /upload-read-chunk-embed-index`

### Retrieval & QA
- `POST /query`
- `POST /answer`

---

## Example Usage

### Query

```json
{
  "question": "What is the goal of this project?",
  "top_k": 3
}

### Answer Response
```json
{
  "question": "What is the goal of this project?",
  "answer": "The goal is to make this project part of my GitHub portfolio.",
  "citations": [
    {
      "doc_name": "long_test.txt",
      "chunk_id": 1,
      "start": 0,
      "end": 300,
      "text_preview": "The goal is to make this project part of my GitHub portfolio."
    }
  ]
}

## How to Run Locally
### 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

### 2. Install dependencies
pip install -r requirements.txt

### 3. Start Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant

### 4. Start FastAPI
python -m uvicorn app.main:app --reload

### 5. Open Swagger UI
http://127.0.0.1:8000/docs

## Notes
Supports .txt and .pdf documents
Uses local embeddings (no external API required)
Retrieval-based answer generation (lightweight, no LLM yet)
Citation metadata enables traceable answers
Designed for clarity, extensibility, and learning

## Roadmap

Planned improvements:

Better chunking strategies (semantic / paragraph-aware)
Improved citation formatting (highlighting)
Evaluation dataset and retrieval metrics
Docker Compose for full stack setup
Cloud deployment
LLM-based answer generation
Frontend UI for document QA

## Why This Project

This project demonstrates:

End-to-end RAG system design
Practical document processing pipeline
Local embedding workflows
Vector database integration (Qdrant)
Retrieval-based QA with citation grounding
Production-style API design with FastAPI

## License

MIT