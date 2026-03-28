
from sentence_transformers import SentenceTransformer
from settings.config import EMBEDDING_MODEL

class EmbeddingModel :
    def __init__(self) :
        self.model = SentenceTransformer(EMBEDDING_MODEL)
    
    def embed(self, chunk_texts) :
        return self.model.encode(chunk_texts, convert_to_tensor = False)
        # return self.model.encode(chunk_texts, convert_to_tensor = False, normalize_embeddings=True)