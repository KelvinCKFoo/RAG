# scripts/ingest_data.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables from .env file
#load_dotenv()

# --- Configuration ---
# ***** UPDATED FILE PATH *****
PDF_PATH = "data/restoring-control-over-the-immigration-system-white-paper.pdf"
PERSIST_DIRECTORY = "backend/chroma_db"

def create_vector_db():
    """
    Creates and persists a Chroma vector database from the specified PDF document.
    """
    if not os.path.exists(PDF_PATH):
        print(f"Error: PDF file not found at {PDF_PATH}")
        return

    print("--- Loading PDF document... ---")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    
    if not documents:
        print("Error: Could not load any documents from the PDF.")
        return

    print(f"--- Loaded {len(documents)} pages from the document. ---")

    print("--- Splitting documents into chunks... ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"--- Split document into {len(chunks)} chunks. ---")

    print("--- Initializing OpenAI embeddings... ---")
    embeddings = OpenAIEmbeddings()

    print(f"--- Creating and persisting vector store at {PERSIST_DIRECTORY}... ---")
    # Create a new Chroma vector store from the chunks and persist it
    # This will overwrite the existing database if you run it again.
    vectordb = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print("--- Vector database creation complete. ---")
    print(f"--- Total vectors in store: {vectordb._collection.count()} ---")

if __name__ == "__main__":
    create_vector_db()