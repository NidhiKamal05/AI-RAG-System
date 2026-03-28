from models.embedding_model import EmbeddingModel
from rag.retriever import Retriever
from rag.guard import Guard

class RagPipeline :
    def __init__(self) :
        pass

    def run(self, query) :
        embedding = EmbeddingModel()
        retriever = Retriever()
        guard = Guard()
        query_embeddings = embedding.embed([query])[0]
        retrieved_chunks = retriever.retrieve(query_embeddings)
        guard_output = guard.filter_chunks(retrieved_chunks)
        return guard_output