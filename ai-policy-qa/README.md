# UK Immigration Policy Q&A 🇬🇧

This is a full-stack web application that uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions about the UK's "Restoring control over the immigration system" white paper. Ask a question in plain English and get an accurate, AI-generated answer sourced directly from the document.

**[Live Demo](https://rag-frontend-uh0g.onrender.com/)**

![App Screenshot](https://i.imgur.com/example-screenshot.png) ---
## 🏛️ Architecture

The application uses a modern, decoupled architecture:

* **Frontend**: A simple interface built with vanilla HTML, CSS, and JavaScript that allows users to submit questions and view answers.
* **Backend API**: A Python backend built with **FastAPI** that exposes a single endpoint (`/ask`) to handle user queries.
* **RAG Pipeline**: The core of the application, orchestrated with **LangChain**. It performs the following steps:
    1.  Loads and chunks the source PDF document.
    2.  Generates vector embeddings using the **OpenAI API**.
    3.  Stores the embeddings in a **ChromaDB** vector store.
    4.  Retrieves relevant document chunks based on the user's question.
    5.  Uses a powerful Language Model (LLM) via the OpenAI API to synthesise a final answer based on the retrieved context.

![Architecture Diagram](https://i.imgur.com/example-diagram.png) ---
## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, LangChain, ChromaDB, OpenAI
* **Frontend:** HTML, CSS, JavaScript
* **Deployment:** Docker, Render (or other cloud service)

---
## 🚀 Running Locally

Follow these instructions to set up and run the project on your local machine.

### Prerequisites
* Git
* Python 3.9+
* Docker

### 1. Clone the Repository
```bash
git clone [https://github.com/KelvinCKFoo/RAG.git](https://github.com/KelvinCKFoo/RAG.git)
cd RAG
```

### 2. Set Up Environment Variables
You will need an OpenAI API key.

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and add your OpenAI API key:
    ```
    OPENAI_API_KEY="sk-..."
    ```
This file is listed in `.gitignore` and will not be committed to the repository.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the Vector Database
The following script will process the PDF in the `/data` directory and create the local vector database. **This only needs to be run once.**
```bash
python scripts/ingest_data.py
```

### 5. Run the Application with Docker (Recommended)
1.  Build the Docker image:
    ```bash
    docker build -t immigration-qa-app .
    ```
2.  Run the Docker container:
    ```bash
    # This command runs the container and injects your API key from the .env file
    docker run --env-file .env -p 8000:8000 immigration-qa-app
    ```

The backend server is now running at `http://127.0.0.1:8000`. Open the `frontend/index.html` file in your browser to use the application.
