# backend/main.py
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from rag_pipeline import get_rag_chain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.error(f"Error initializing RAG chain: {e}")
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
    logger.info(f"Received question: {request.question}")

    if rag_chain is None:
        logger.error("RAG chain is not available. Check server logs for initialization errors.")
        raise HTTPException(
            status_code=500,
            detail="RAG chain is not available. Check server logs for initialization errors."
        )

    # ***** NEW: ADDED DETAILED ERROR LOGGING *****
    try:
        logger.info("Invoking RAG chain...")
        result = rag_chain.invoke({"input": request.question})
        logger.info("RAG chain invocation successful.")

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
        # This will log the full error traceback to your terminal
        logger.error(f"An error occurred during RAG chain invocation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the request.")