from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.services.parser import extract_text
from app.services.chunker import chunk_text

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-read-chunk")
async def upload_read_chunk(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)

    try:
        text = extract_text(file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    chunks = chunk_text(text=text, chunck_size=300, overlap=50)

    return {
        "filename": file.filename,
        "num_characters": len(text),
        "num_chunks": len(chunks),
        "chunks": chunks[:5]
    }