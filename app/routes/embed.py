from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.services.parser import extract_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_texts

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-read-chunk-embed")
async def upload_read_chunk_embed(file: UploadFile = File(...)):
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

    results = []
    for chunk, embedding in zip(chunks, embeddings):
        results.append({
            "chunk_id": chunk["chunk_id"],
            "text_preview": chunk["text"][:120],
            "embedding_dimension": len(embedding),
            "embedding_preview": embedding[:5]
        })
    
    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "results": results[:5]
    }