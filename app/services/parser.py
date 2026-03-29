from pathlib import Path
import fitz #PyMuPDF

def read_text_file(file_path: Path) -> str:
    with open(file_path,'r', encoding='utf-8') as f:
        return f.read()
    
def read_pdf_file(file_path: Path) -> str:
    text = []
    doc = fitz.open(file_path)
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)

def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == '.txt':
        return read_text_file(file_path)
    elif suffix == '.pdf':
        return read_pdf_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")