from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.services.parser import extract_text

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-and-read")
async def upload_and_read(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    
    try:
        text = extract_text(file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "filename": file.filename,
        "save_to": str(file_path),
        "preview": text[:1000],
        "num_characters": len(text)
    }