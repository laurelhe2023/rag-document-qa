from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedder import embed_query
from app.services.vector_store import search_chunks

router = APIRouter()

class AnswerRequest(BaseModel):
    question: str
    top_k: int = 3

def extract_best_sentence(text: str) -> str:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    if not sentences:
        return text
    return sentences[-1] + "."

@router.post("/answer")
async def answer_question(request: AnswerRequest):
    query_embedding = embed_query(request.question)
    results = search_chunks(query_embedding=query_embedding, limit=request.top_k)

    if not results:
        return {
            "question": request.question,
            "answer": "No relevant information found.",
            "citations": []
        }
    
    top_result = results[0]
    short_answer = extract_best_sentence(top_result["text"])

    return {
        "question": request.question,
        "answer": short_answer,
        "citations":[
            {
                "doc_name": top_result["doc_name"],
                "chunk_id": top_result["chunk_id"],
                "start": top_result["start"],
                "end": top_result["end"],
                "text_preview": top_result["text"][:120]
            }
        ],
        "retrieved_results": results
    }