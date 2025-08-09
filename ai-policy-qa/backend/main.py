# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from rag_pipeline import get_rag_chain

# --- API METADATA ---
app = FastAPI(
    title="UK Immigration Policy Q&A API",
    description="An API for asking questions about the UK's 'Restoring control over the immigration system' white paper.",
    version="1.0.0",
)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Request and Response ---
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    source_documents: List[Dict[str, Any]]

# --- Load RAG Chain on Startup ---
try:
    rag_chain = get_rag_chain()
except FileNotFoundError as e:
    print(f"Error initializing RAG chain: {e}")
    rag_chain = None

# --- API Endpoints ---
@app.get("/", summary="Root endpoint to check API status")
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"status": "ok", "message": "Welcome to the UK Immigration Policy Q&A API!"}


@app.post("/ask", response_model=QueryResponse, summary="Ask a question")
async def ask_question(request: QueryRequest):
    """
    Receives a question, processes it through the RAG pipeline,
    and returns the answer along with source documents.
    """
    if rag_chain is None:
        raise HTTPException(
            status_code=500,
            detail="RAG chain is not available. Check server logs for initialization errors."
        )

    try:
        result = rag_chain.invoke({"input": request.question})

        # Format source documents for the response
        source_docs = []
        for doc in result.get("context", []):
            source_docs.append(
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                }
            )

        return QueryResponse(
            answer=result.get("answer", "No answer found."),
            source_documents=source_docs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")