from typing import List, Dict

def chunk_text(
        text: str, 
        chunck_size: int = 300, 
        overlap: int = 50,
        min_chunk_length: int = 50
    ) -> List[Dict]:
    if chunck_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunck_size:
        raise ValueError("overlap must be smaller than chunk_size")
    
    chunks = []
    start = 0
    chunk_id = 1
    step = chunck_size - overlap

    while start < len(text):
        end = start + chunck_size
        chunk = text[start:end]

        if len(chunk.strip()) < min_chunk_length:
            break

        chunks.append({
            "chunk_id": chunk_id,
            "start": start,
            "end": min(end, len(text)),
            "text": chunk
        })

        start += step
        chunk_id += 1
    
    return chunks