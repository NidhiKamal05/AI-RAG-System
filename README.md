# AI RAG System


---

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline using Python documentation as the knowledge base.

It transforms raw text into embeddings, stores them in a vector database, retrieves the most relevant chunks, and <b>generates answers using an LLM</b> based on the retrieved context.

### Built to simulate a semantic search + generation system with confidence-based filtering and controlled hallucination for better accuracy.


---

## Run on Colab

[![Open In 
Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NidhiKamal05/AI-RAG-System/blob/main/notebook.ipynb)


---

## Architecture

<p align="center">
	<img src="assets/rag_pipeline_architecture.png" width="700"/>
	<br>
	<em>End-to-End RAG Pipeline Architecture</em>
	<br>
	<sub>Diagram generated using ChatGPT (OpenAI)</sub>
</p>


---

## Tech Stack

- Python

- Transformers (AutoTokenizer)

- Sentence Transformers (all-MiniLM-L6-v2)

- ChromaDB (Vector Database)

- TinyLlama (TinyLlama/TinyLlama-1.1B-Chat-v1.0)

- Google Colab

- Google Drive



---

## Google Colab + Drive Integration

This project is implemented and tested entirely on Google Colab with dataset stored in Google Drive.

### Setup

from google.colab import drive
drive.mount('/content/drive')

DATA_PATH = "/content/drive/MyDrive/your_project_folder/"

- Enables seamless file access and persistence


---

## Project Workflow

### Data Cleaning

- Removed \r

- Split using \n

- Stripped whitespace

- Rejoined cleaned text



---

### Chunking

- Implemented token-based chunking with overlap (fixed size strategy)

- Tokenizer: TinyLlama (via Transformers)

- Chunk size: 400 tokens

- Overlap: 50 tokens


---

### Embeddings

- Model: all-MiniLM-L6-v2 (via Sentence Transformers)

- Converts text → vectors

- Normalized for cosine similarity



---

### Data Ingestion

- Reads files from Google Drive


- Applies:

	- Cleaning

	- Chunking

	- Embedding


- Stores:

	- Text

	- Embeddings

	- Metadata



---

### Retrieval

- Database: ChromaDB

- Metric: Cosine Similarity

- Top K: 3


- Process:

	- Query → embedding

	- Similarity search

	- Return top chunks



---

### Guard System (Key Feature 🔥)

- Improves reliability and reduces hallucination using confidence scoring

1. Logic:

	- Compare top 2 similarity scores

	- Compute difference (gap)


2. Confidence Levels:

	- High score: similarity > 0.42 AND gap > 0.01
	- Medium score: similarity > 0.42 AND gap <= 0.01
	- Low Ignored


→ Filters irrelevant results
→ Ensures better precision



---

### Generation (LLM Layer)

- Model: TinyLlama/TinyLlama-1.1B-Chat-v1.0

#### Context Building

- Uses maximum 2 chunks with high confidence

- Includes:

	- Chunk document
	- Chunk ID

#### Generation Settings

- MAX NEW TOKENS: 350

- TEMPERATURE: 0.2

- DO SAMPLE: False

- REPETITION PENALTY: 1.1

- MAX TIME: 100

- MAX GENERATION TIME: 45

#### Flow

- Build prompt from retrieved chunks

- Pass to LLM (llm_model.py)

- If generation succeeds → return answers

- Else → return refusal message



---

### Pipeline

####Query → Embedding → Retrieval → Guard → Context Building → Generation(LLM) → Output####

#### Flow:

1. Retrieve chunks
2. If no chunks → return final output with refusal
3. Apply Guard
4. If Guard fails → return final output(with retrieved chunks and medium confidence) with refusal
5. Else → Generate answers
6. Return final output

#### Latency Tracking

- Total latency
- Retrieval latency
- Generation latency

-- If generation latency > 45 seconds → add fault: "GENERATION SLOW"



---

### Final Output

Contains:
- Query
- Answer
- Retrieved chunks
- Confidence level
- Latency (total, retrieval, generation)
- Faults (if any)



---

## Project Structure

AI-RAG-System/
- data/
	- text/
        - (Python tutorial files)

- db/
    - chroma_db/
        - (stored embeddings collection)

- ingestion/
	- __init__.py
	- chunk.py
	- ingestion.py

- models/
	- __init__.py
	- embedding_model.py
	- llm_model.py

- pipeline/
	- __init__.py
	- pipeline.py

- rag/
	- __init__.py
	- guard.py
	- retriever.py
	- generator.py

- settings/
	- __init__.py
	- config.py

- notebook.ipynb



---

### Structure Explanation

- data/ → Contains raw dataset (Python documentation)

- db/ → Stores vector database (ChromaDB embeddings)

- ingestion/ → Handles cleaning, chunking, and data ingestion

- models/ → Embedding model logic

- pipeline/ → End-to-end RAG pipeline

- rag/ → Core retrieval + guard logic

- settings/ → Configuration (thresholds, paths, etc.)

- notebook.ipynb → Colab notebook for running and testing



---

## Features

- End-to-end RAG pipeline

- Semantic search system + LLM generation

- Token-based chunking with overlap

- Confidence-based filtering (Guard)

- Hallucination control mechanism

- Latency monitoring & fault detection

- Modular architecture

- Google Colab + Drive integration



---

## Experimentation

- Tested with multiple queries


→ Tuned:

	- Similarity Threshold = 0.42

	- Gap = 0.01



---

## Use Cases

- Query Python documentation intelligently

- Semantic search engine

- Base for chatbot systems



---

## Future Improvements

- Build UI

- Hybrid search

- Implement semantic chunking

- Improve ranking mechanism


---

## Author

Nidhi Kamal


---

## Support

If you found this project helpful:<br>
⭐ Star this repository<br>
🔗 Share it on LinkedIn<br>


---
