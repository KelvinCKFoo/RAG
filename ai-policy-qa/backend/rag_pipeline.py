# backend/rag_pipeline.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load environment variables
#load_dotenv()

# --- Configuration ---
# ***** CORRECTED FILE PATH *****
PERSIST_DIRECTORY = "chroma_db" 
LLM_MODEL = "gpt-5-nano"

def get_rag_chain():
    """
    Initializes and returns a RAG (Retrieval-Augmented Generation) chain.
    """
    if not os.path.exists(PERSIST_DIRECTORY):
        raise FileNotFoundError(
            f"ChromaDB persistence directory not found at '{PERSIST_DIRECTORY}'. "
            "Please run the ingestion script first (scripts/ingest_data.py)."
        )
    # ... (the rest of the file is unchanged) ...
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    
    llm = ChatOpenAI(model_name=LLM_MODEL, temperature=0.1)

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    system_prompt = (
        "You are an expert assistant for answering questions about UK government policy. "
        "Use the provided context from the 'Restoring control over the immigration system' white paper to answer the question. "
        "If the answer is not in the context, state that you cannot find the information in the document. "
        "Be concise and base your answer *only* on the provided text.\n\n"
        "Context:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    
    Youtube_chain = create_stuff_documents_chain(llm, prompt)
    
    rag_chain = create_retrieval_chain(retriever, Youtube_chain)
    
    return rag_chain