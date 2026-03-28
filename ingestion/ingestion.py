
from models.embedding_model import EmbeddingModel
from ingestion.chunk import Chunk
from settings.config import DOCS_PATH
from rag.retriever import Retriever
import os
import uuid

DOCS_PATH = DOCS_PATH

def ingest_documents() :

    chunker = Chunk()
    embedding_model = EmbeddingModel()
    retriever = Retriever()

    all_chunks = 0
    total_files = 0
    chunk_per_file = []

    for filename in os.listdir(DOCS_PATH) :

        filepath = os.path.join(DOCS_PATH, filename)

        if not os.path.isfile(filepath) :
            continue
        
        with open(filepath, "r", encoding = "utf-8") as f :
            total_files += 1

            text = f.read()
            cleaned_text = chunker.clean_text(text)
            chunks = chunker.chunk_text(cleaned_text)
            total_chunks = len(chunks)

            all_chunks += total_chunks
            chunk_per_file.append({"source": filename, "total_chunks": total_chunks})

            for idx, chunk in enumerate(chunks) :
                embedding = embedding_model.embed([chunk])[0]
                metadata = {"source": filename, "total_chunks": total_chunks, "chunk_id": idx}
                retriever.collection.add(ids = [str(uuid.uuid4())], documents = [chunk], embeddings = [embedding], metadatas = [metadata])
    
    print(f"INGESTION COMPLETE..... Total Chunks = {all_chunks}")

    return {"total_files_read": total_files, "total_chunks_read": all_chunks, "chunk_per_file": chunk_per_file}