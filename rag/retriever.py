import chromadb
from chromadb.config import Settings
from settings.config import CHROMA_DB_PATH, TOP_K

class Retriever :
    def __init__(self) :
        self.client = chromadb.PersistentClient(path = CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(name = "knowledge", metadata = {"hnsw:space":"cosine"})
    
    def retrieve(self, query_embeddings) :
        results = self.collection.query(query_embeddings = [query_embeddings], n_results = TOP_K, include = ["documents", "metadatas", "distances"])
        return results