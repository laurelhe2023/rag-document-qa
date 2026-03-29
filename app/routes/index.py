from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.services.parser import extract_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_texts
from app.services.vector_store import ensure_collection, upsert_chunks

router = APIRouter()

UPLOAD_DIR = Path('data/uploads')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-read-chunk-embed-index")
async def upload_read_chunk_embed_index(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    
    try:
        text = extract_text(file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    chunks = chunk_text(text=text, chunck_size=300, overlap=50)
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(chunk_texts)

    ensure_collection(vector_size=len(embeddings[0]))
    upsert_chunks(chunks=chunks, embeddings=embeddings, doc_name=file.filename)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "status": "indexed into qdrant"
    }