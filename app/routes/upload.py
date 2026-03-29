from fastapi import APIRouter, UploadFile, File
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)

    return {
        'filename': file.filename,
        'saved_to': str(file_path)
    }