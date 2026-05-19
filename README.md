# ScholarRAG: Local Research Paper Assistant for AI and Data Science Papers

ScholarRAG is a local end-to-end Retrieval-Augmented Generation, or RAG, application that allows users to ask questions over a large research paper knowledge base. The system collects AI and Data Science research papers from arXiv, extracts text from PDFs, chunks the content, creates embeddings, stores them in a FAISS vector index, retrieves relevant chunks for a user question and uses a local LLM through Ollama to generate citation-grounded answers.

This project was built as a hands-on local RAG pipeline to understand how document ingestion, semantic search, retrieval, prompt construction and answer generation work together in a real application.

---

## Project Status

Current working version includes:

- arXiv paper collection by topic
- Local PDF download and storage
- PDF text extraction using PyMuPDF
- Text chunking with overlap
- Embedding generation using `BAAI/bge-small-en-v1.5`
- FAISS vector index creation
- Semantic retrieval over 16,000+ chunks
- Local answer generation using Ollama and Llama 3.1 8B
- FastAPI backend with `/ask` endpoint
- Streamlit frontend for asking questions and viewing sources
- Progress screenshots stored for documentation

Current local knowledge base:

```text
210 research papers
16,544 text chunks
16,544 FAISS vectors
Embedding dimension: 384
```

---

## Why I Built This

Most basic RAG tutorials use a few small documents and focus only on the final chatbot response. I wanted to build something closer to a real research assistant with a larger local knowledge base and a full pipeline behind it.

The goal of this project was to understand and implement the complete RAG workflow:

```text
raw research papers → text extraction → chunking → embeddings → vector search → retrieved context → local LLM answer → source-backed response
```

I also wanted the system to run locally instead of depending completely on cloud APIs. This makes the project useful for learning how local AI applications work, how retrieval affects answer quality and how source grounding can reduce unsupported responses.

The project focuses on AI and Data Science research areas such as:

- Large Language Models
- Retrieval-Augmented Generation
- Natural Language Processing
- Machine Learning
- Data Analysis
- Information Retrieval
- Databases and Vector Search

---

## Features

### 1. arXiv Paper Collection

The project includes a script to collect research papers from arXiv by topic.

Topics currently used:

```text
llm
rag
nlp
machine_learning
data_analysis
information_retrieval
databases
```

Each topic downloads papers into its own folder:

```text
data/raw_papers/
├── data_analysis/
├── databases/
├── information_retrieval/
├── llm/
├── machine_learning/
├── nlp/
└── rag/
```

The paper metadata is saved locally, including:

- topic
- arXiv ID
- title
- authors
- published date
- abstract
- PDF URL
- local PDF path

---

### 2. PDF Text Extraction

The PDFs are processed using PyMuPDF. Each paper is converted into extracted text and saved as JSON.

The extraction pipeline reads from:

```text
data/raw_papers/
```

and writes extracted text to:

```text
data/processed_chunks/extracted_text/
```

Each extracted JSON file contains:

```json
{
  "topic": "rag",
  "source_pdf": "path/to/paper.pdf",
  "text": "extracted paper text"
}
```

---

### 3. Chunking

Long paper text is split into smaller overlapping chunks.

Current chunking settings:

```text
chunk_size = 1200 characters
overlap = 200 characters
```

This helps preserve context across chunk boundaries while keeping each chunk small enough for retrieval and prompt construction.

The chunked output is saved to:

```text
data/processed_chunks/chunks/
```

Each chunk contains:

```json
{
  "chunk_id": "paper_chunk_0",
  "topic": "rag",
  "source_pdf": "path/to/paper.pdf",
  "chunk_index": 0,
  "text": "chunk text"
}
```

---

### 4. Embeddings

The project uses:

```text
BAAI/bge-small-en-v1.5
```

from SentenceTransformers to convert text chunks into dense vector embeddings.

The embeddings are normalized before being stored in FAISS. This allows similarity search using inner product search.

---

### 5. FAISS Vector Index

The generated embeddings are stored in a FAISS index.

Output files:

```text
data/faiss_index/research_papers.index
data/faiss_index/chunk_metadata.pkl
```

The FAISS index stores the vectors, while the metadata file maps each vector back to its original chunk, topic and source PDF.

These files are not pushed to GitHub because they are generated locally and can become large.

---

### 6. Retriever

The retriever loads:

```text
research_papers.index
chunk_metadata.pkl
```

Then it takes a user query, embeds the query and searches FAISS for the top matching chunks.

Example query:

```text
What is retrieval augmented generation?
```

Example retrieved result:

```text
Topic: rag
Source: Why Retrieval-Augmented Generation Fails: A Graph Perspective
Score: 0.8431
```

---

### 7. Local LLM Answer Generation

The app uses Ollama to run a local LLM.

Current model:

```text
llama3.1:8b
```

The generator builds a prompt using the retrieved chunks and asks the local LLM to answer using only the provided research paper excerpts.

The prompt instructs the model to:

- answer only from retrieved context
- avoid unsupported claims
- cite sources using `[1]`, `[2]`, `[3]`
- avoid inventing papers, methods, numbers or citations
- admit when the provided context is incomplete

---

### 8. FastAPI Backend

The backend exposes an `/ask` endpoint.

Example request:

```json
{
  "question": "What is retrieval augmented generation?",
  "top_k": 5
}
```

Example response structure:

```json
{
  "question": "What is retrieval augmented generation?",
  "answer": "Generated answer with citations...",
  "sources": [
    {
      "source_id": 1,
      "score": 0.8431,
      "topic": "rag",
      "source_pdf": "data/raw_papers/rag/example.pdf",
      "chunk_index": 0,
      "text_preview": "Retrieved text preview..."
    }
  ]
}
```

---

### 9. Streamlit Frontend

The frontend provides a simple chatbot interface where users can:

- enter a research question
- choose the number of retrieved chunks
- view the generated answer
- expand retrieved sources
- inspect source PDF paths, scores, topics and text previews

---

## Current Architecture

```text
arXiv Papers
     ↓
PDF Download
     ↓
PDF Text Extraction
     ↓
Text Chunking
     ↓
Embedding Generation
     ↓
FAISS Vector Index
     ↓
User Question
     ↓
Query Embedding
     ↓
Top-K Retrieval
     ↓
Prompt Construction
     ↓
Ollama / Local LLM
     ↓
Answer + Sources
     ↓
Streamlit UI
```

---

## Project Structure

```text
scholar-rag/
│
├── backend/
│   ├── arxiv_collector.py
│   ├── pdf_loader.py
│   ├── process_papers.py
│   ├── chunker.py
│   ├── create_chunks.py
│   ├── embedder.py
│   ├── build_vector_index.py
│   ├── retriever.py
│   ├── generator.py
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── raw_papers/
│   ├── processed_chunks/
│   ├── faiss_index/
│   └── metadata/
│
├── docs/
│   └── screenshots/
│
├── evaluation/
│
├── notebooks/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Screenshots

### Streamlit Chatbot Interface

![Streamlit Chatbot UI](docs/screenshots/02-streamlit-chatbot-ui.png)

### FastAPI Swagger Response

![FastAPI Swagger Response](docs/screenshots/01-fastapi-swagger-response.png)

Add or rename screenshots as needed inside:

```text
docs/screenshots/
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Sindura06/scholar-rag.git
cd scholar-rag
```

---

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Ollama

Download and install Ollama from:

```text
https://ollama.com
```

Then pull the local LLM:

```bash
ollama pull llama3.1:8b
```

Check installed models:

```bash
ollama list
```

---

## How to Rebuild the Knowledge Base

The actual PDFs, processed chunks and FAISS index are not included in GitHub. They are ignored intentionally to keep the repository lightweight.

To rebuild the local knowledge base, run the pipeline in this order.

---

### Step 1: Collect arXiv Papers

```bash
python backend/arxiv_collector.py
```

This downloads research papers by topic into:

```text
data/raw_papers/
```

It also saves paper metadata into:

```text
data/metadata/arxiv_metadata.csv
```

---

### Step 2: Extract Text from PDFs

```bash
python backend/process_papers.py
```

This extracts paper text and saves JSON files into:

```text
data/processed_chunks/extracted_text/
```

---

### Step 3: Create Text Chunks

```bash
python backend/create_chunks.py
```

This creates searchable chunks and saves them into:

```text
data/processed_chunks/chunks/
```

---

### Step 4: Build the FAISS Vector Index

```bash
python backend/build_vector_index.py
```

This creates:

```text
data/faiss_index/research_papers.index
data/faiss_index/chunk_metadata.pkl
```

For the current run, this created:

```text
16,544 vectors
384-dimensional embeddings
```

---

## Running the Application

You need two terminals.

---

### Terminal 1: Start FastAPI Backend

Do not use `--reload` for this project because the backend loads FAISS and the embedding model. On some systems, especially macOS, reload can repeatedly spawn Python processes and cause crashes.

Use:

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

---

### Terminal 2: Start Streamlit Frontend

Activate the environment again:

```bash
source venv/bin/activate
```

Run Streamlit:

```bash
streamlit run frontend/app.py
```

Then ask a question such as:

```text
What is retrieval augmented generation?
```

---

## Important GitHub Notes

The following are intentionally ignored and not pushed to GitHub:

```text
data/raw_papers/
data/processed_chunks/
data/faiss_index/
data/metadata/
.env
venv/
__pycache__/
```

This is because the paper PDFs, extracted text, chunks and FAISS index can become large and should be generated locally.

The repository contains the code needed to recreate the full pipeline.

---

## Current Limitations

The current version works end to end, but there are areas for improvement:

1. Some retrieved chunks may come from bibliography or reference sections.
2. The generated answer quality depends heavily on retrieved chunk quality.
3. The chunking method currently uses character-based chunking, not section-aware chunking.
4. Source citations currently point to local PDF paths and chunk indexes, not exact page-level citations.
5. The system does not yet include reranking.
6. The system does not yet include evaluation metrics such as Top-K source presence or unsupported answer rate.

---

## Planned Improvements

Future improvements include:

- filter low-quality chunks such as references and bibliography
- add section-aware chunking for abstracts, methods, results and conclusions
- add page-level citation tracking
- add reranking using a cross-encoder model
- add topic filters in the UI
- add chat history
- add benchmark questions for evaluation
- measure retrieval accuracy
- measure unsupported response rate
- improve prompt grounding
- add support for user-uploaded PDFs
- add PostgreSQL or SQLite for persistent metadata and chat history

---

## Skills Demonstrated

This project demonstrates:

- Retrieval-Augmented Generation
- Local LLM application development
- PDF ingestion
- arXiv data collection
- Text preprocessing
- Semantic chunking
- Embedding generation
- FAISS vector search
- Prompt engineering
- FastAPI backend development
- Streamlit frontend development
- Local AI system design
- Source-grounded answer generation
- Git and GitHub workflow

---

## Tech Stack

```text
Python
FastAPI
Streamlit
FAISS
SentenceTransformers
BAAI/bge-small-en-v1.5
Ollama
Llama 3.1 8B
PyMuPDF
arxiv Python package
requests
NumPy
```

---

## Collaboration

I am open to collaboration on this project.

Possible collaboration areas:

- improving retrieval quality
- adding reranking
- building a better frontend
- adding evaluation metrics
- expanding the research paper dataset
- improving chunking strategies
- adding support for user-uploaded PDFs
- deploying a lightweight demo version
- integrating database-backed chat history

If you are interested in contributing, feel free to open an issue, suggest improvements or submit a pull request.

---

## Author

Built by Sindura.

GitHub: [Sindura06](https://github.com/Sindura06)

---

## Disclaimer

This project is for learning, research and portfolio purposes. The generated answers depend on the retrieved paper chunks and should be verified against the original papers before being used for academic or professional decisions.