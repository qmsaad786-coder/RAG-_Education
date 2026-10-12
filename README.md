# Education RAG System

An AI-powered curriculum and course-content retrieval system. Ask questions about the included university syllabus PDFs and receive answers grounded in the retrieved document content.

## Problem Statement

University curricula are commonly distributed as long PDF documents, making it slow to locate information such as subjects, units, prerequisites, or course content. This project provides a natural-language interface that searches syllabus documents and produces context-aware answers.

## Architecture

```text
Syllabus PDFs (data/)
        |
        v
PyPDFLoader -> document metadata -> text chunking
        |                              |
        +-----------> MiniLM embeddings v
                            |
                            v
                  Chroma vector database (chroma_db/)
                            |
User question + optional university filter
                            |
                            v
                     Similarity retrieval (top 4)
                            |
                            v
              Prompt with retrieved context -> Gemini 2.5 Flash
                            |
                            v
                    Streamlit answer interface
```

## Tech Stack

- **Interface:** Streamlit
- **RAG orchestration:** LangChain
- **Document loading:** PyPDF / LangChain `PyPDFLoader`
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector database:** ChromaDB
- **LLM:** Google Gemini 2.5 Flash
- **Language:** Python

## Features

- Answers academic queries from the supplied syllabus PDFs.
- Automatically indexes PDFs when no vector database exists.
- Persists embeddings locally in `chroma_db/` for subsequent runs.
- Filters results by university or searches all available documents.
- Retrieves the four most relevant chunks for each question.
- Uses a grounded prompt that returns a clear fallback when the answer is unavailable in the syllabus context.

## RAG / LLM Workflow

1. Each PDF in `data/` is loaded page by page.
2. The source file name is saved as `university` metadata on every page.
3. Pages are split into 1,000-character chunks with 200-character overlap.
4. Chunks are embedded with MiniLM and stored in ChromaDB.
5. A question is used to retrieve the four most relevant chunks, optionally limited to the selected university.
6. The retrieved text and question are placed in a prompt instructing Gemini to answer only from the supplied context.
7. Gemini generates the final answer, which is displayed in the Streamlit UI.

## Project Structure

```text
rag_education/
├── app.py                 # Streamlit entry point
├── data/                  # University syllabus PDFs
├── src/
│   ├── config.py           # Paths, model, chunking, and retrieval settings
│   ├── document_loader.py  # PDF loading and metadata assignment
│   ├── text_splitter.py    # Document chunking
│   ├── embedding_model.py  # Embedding-model configuration
│   ├── vector_store.py     # Chroma creation and loading
│   ├── retriever.py        # Similarity search and university filtering
│   ├── rag_pipeline.py     # Prompt and RAG chain
│   └── llm.py              # Gemini integration
└── requirements.txt
```

## Screenshots

Add application screenshots to a `screenshots/` directory and reference them here. For example:

```md
![Education RAG interface](screenshots/home.png)
```

## Installation

### Prerequisites

- Python 3.10 or later
- A Google Gemini API key

### Setup

```powershell
git clone <your-repository-url>
cd rag_education
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Place syllabus PDFs in `data/`. The file name becomes the university name shown in the filter.

## How to Run

From the project root, with the virtual environment activated:

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, choose a university if desired, enter an academic question, and select **Ask**.

On the first run, the application builds the local Chroma index from the PDFs. To re-index after changing documents, delete the `chroma_db/` directory and run the application again.

## Results

The system provides syllabus-grounded responses to queries such as:

- “What subjects are included in the data science curriculum?”
- “Which unit covers operating systems?”
- “What course content is listed for a selected university?”

Answers are based on the retrieved PDF chunks. When the required information is absent, the assistant responds: `Information not found in the provided syllabus documents.`

## Future Improvements

- Display source document names, page numbers, and retrieval citations with every answer.
- Add document upload and in-app re-indexing.
- Use hybrid search and reranking to improve retrieval accuracy.
- Add chat history, saved queries, and comparison views across universities.
- Evaluate responses with a labelled question-and-answer dataset.
- Add authentication and deploy the app for multi-user access.
- Add tests, logging, error handling, and configuration for multiple LLM providers.
