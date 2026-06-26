# AI Learning Assistant

An AI-powered learning assistant for textbooks, lecture notes, and educational documents using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

The system automatically extracts educational content, generates hierarchical summaries, builds a searchable vector database, creates AI-generated flashcards for active recall, and enables question answering over uploaded learning materials through an interactive Streamlit interface.

---

## Features

* 📚 Automatic textbook and document extraction
* 📝 Hierarchical chapter and section summarization
* 💬 RAG-based Question Answering
* 🧠 AI-generated flashcards for active recall
* 📊 Figure and table caption extraction
* 📖 Interactive learning library
* 🌐 Streamlit-based user interface

---

## How It Works

```text
Educational Documents (PDF)
             │
             ▼
Content Extraction
(Text, Figures, Tables)
             │
             ▼
Section Detection
             │
             ▼
Hierarchical Summarization
             │
     ┌───────┴────────┐
     ▼                ▼
Vector Database     Flashcard
 (ChromaDB)        Generation (LLM)
     │
     ▼
RAG Question Answering
```

---

## Features Overview

### Hierarchical Summarization

Large documents are automatically divided into logical sections. Each section is summarized individually before producing an overall document summary, preserving the structure and key concepts of the learning material.

### AI Flashcards

The assistant generates question-answer flashcards directly from each major section of the document. The generated flashcards are designed to promote active recall and improve long-term retention.

### RAG-based Question Answering

Users can ask natural language questions about any uploaded document. Relevant passages are retrieved from the vector database and combined with an LLM to generate accurate, context-aware answers.

---

## Technologies

* Python
* Streamlit
* LangChain
* Google Gemini
* Ollama
* ChromaDB
* Hugging Face
* Poetry

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Hosein541/ai-learning-assistant.git
cd ai-learning-assistant
```

### Install dependencies

```bash
pip install poetry
poetry install
```

### Install the embedding model

Make sure Ollama is installed and running.

```bash
ollama pull embeddinggemma
```

Start the Ollama server:

```bash
ollama serve
```

### Launch the application

```bash
poetry run streamlit run app.py
```

---

## Requirements

Before starting a session, provide:

* Google Gemini API Key
* Hugging Face Access Token

These credentials are entered through the application interface and are used only during the current session.

---

## Project Structure

```text
extractor/        # PDF extraction pipeline
summarize/        # Hierarchical summarization
flashcards/       # Flashcard generation
qa_chain/         # RAG question answering
vector_db/        # Chroma vector database
pages/            # Streamlit pages
inputs/           # Uploaded documents
outputs/          # Generated artifacts
pipeline.py       # Main processing pipeline
app.py            # Streamlit application
```

---

## Application Workflow

1. Upload one or more educational documents.
2. Configure the required API keys.
3. Start a processing session.
4. The system automatically:

   * extracts document contents,
   * detects document sections,
   * generates hierarchical summaries,
   * builds the vector database,
   * creates AI-generated flashcards.
5. Explore the processed documents through:

   * Library
   * Question Answering
   * Flashcards

---

## License

This project is intended for educational and learning purposes.
