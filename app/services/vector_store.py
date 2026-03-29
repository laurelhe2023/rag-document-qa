from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict

COLLECTION_NAME = "documents"

client = QdrantClient(host="localhost", port=6333)

def ensure_collection(vector_size: int = 384):
    collections_response = client.get_collections()
    existing_names = [c.name for c in collections_response.collections]

    if COLLECTION_NAME not in existing_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def upsert_chunks(chunks: List[Dict], embeddings: List[List[float]], doc_name: str):
    points = []

    for chunk, embedding in zip(chunks, embeddings):
        point = PointStruct(
            id=chunk["chunk_id"],
            vector=embedding,
            payload={
                "doc_name": doc_name,
                "chunk_id": chunk["chunk_id"],
                "start": chunk["start"],
                "end": chunk["end"],
                "text": chunk["text"],
            },
        )
        points.append(point)
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

def search_chunks(query_embedding: List[float], limit: int = 3):
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
    )

    formatted = []
    for r in response.points:
        formatted.append({
            "score": r.score,
            "doc_name": r.payload.get("doc_name"),
            "chunk_id": r.payload.get("chunk_id"),
            "start": r.payload.get("start"),
            "end": r.payload.get("end"),
            "text": r.payload.get("text"),
        })
    
    return formatted