from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.read import router as read_router
from app.routes.chunk import router as chunk_router
from app.routes.embed import router as embed_router
from app.routes.index import router as index_router
from app.routes.query import router as query_router
from app.routes.answer import router as answer_router

app = FastAPI(title='RAG Document QA')

@app.get("/")
def root():
    return{"message":"RAG Document QA is running"}

@app.get('/health')
def health():
    return{'status':'ok'}

app.include_router(upload_router)
app.include_router(read_router)
app.include_router(chunk_router)
app.include_router(embed_router)
app.include_router(index_router)
app.include_router(query_router)
app.include_router(answer_router)