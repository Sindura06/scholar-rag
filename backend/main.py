from fastapi import FastAPI
from pydantic import BaseModel

from backend.retriever import Retriever
from backend.generator import generate_answer


app = FastAPI(
    title="ScholarRAG API",
    description="Local RAG assistant for AI and Data Science research papers",
    version="1.0.0"
)


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


class Source(BaseModel):
    source_id: int
    score: float
    topic: str
    source_pdf: str
    chunk_index: int
    text_preview: str


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]


retriever = Retriever()


@app.get("/")
def home():
    return {
        "message": "ScholarRAG API is running",
        "docs": "/docs"
    }


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    retrieved_chunks = retriever.search(
        query=request.question,
        top_k=request.top_k
    )

    answer = generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    sources = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        sources.append(
            Source(
                source_id=i,
                score=chunk["score"],
                topic=chunk["topic"],
                source_pdf=chunk["source_pdf"],
                chunk_index=chunk["chunk_index"],
                text_preview=chunk["text"][:500]
            )
        )

    return AskResponse(
        question=request.question,
        answer=answer,
        sources=sources
    )