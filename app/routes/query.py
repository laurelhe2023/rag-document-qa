from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedder import embed_query
from app.services.vector_store import search_chunks

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

@router.post("/query")
async def query_docs(request: QueryRequest):
    query_embedding = embed_query(request.question)
    results = search_chunks(query_embedding=query_embedding, limit=request.top_k)

    return {
        "question": request.question,
        "num_results": len(results),
        "results": results
    }