from models.embedding_model import EmbeddingModel
from rag.retriever import Retriever
from rag.guard import Guard
from rag.generator import Generator
from settings.config import MAX_GENERATION_TIME, REFUSAL_MESSAGE
from datetime import datetime
import time

class RAGPipeline :
    def __init__(self) :
        pass
	
    def run(self, query) :
        embedding = EmbeddingModel()
        retriever = Retriever()
        guard = Guard()
        generator = Generator()
	  	  
        latency = {'total': 0.0, 'retrieval': 0.0, 'generation': 0.0}
        faults = []
        final_output = {'query': query, 'answer': REFUSAL_MESSAGE, 'latency': latency, 'retrieved_chunks': [], 'faults': faults, 'confidence': "LOW"}
        
        total_start_time = time.time()
        
        query_embeddings = embedding.embed([query])[0]
        
        retrieval_start_time = time.time()
        
        retrieved_chunks = retriever.retrieve(query_embeddings)

        if not retrieved_chunks or len(retrieved_chunks) < 1 :
            latency['total'] = round(time.time() - total_start_time, 3)
            return final_output

        guard_output = guard.filter_chunks(retrieved_chunks)

        if not guard_output or len(guard_output) < 1 :
            final_output['retrieved_chunks'] = retrieved_chunks
            latency['total'] = round(time.time() - total_start_time, 3)
            return final_output
        
        latency['retrieval'] = round(time.time() - retrieval_start_time, 3)

        if guard_output[0]['confidence'] == "MEDIUM" :
            final_output['retrieved_chunks'] = guard_output
            final_output['confidence'] = "MEDIUM"
            latency['total'] = round(time.time() - total_start_time, 3)
            return final_output
        
        generation_start_time = datetime.now()
        generated_text = generator.generation(query, guard_output)
        generation_end_time = datetime.now()
        
        latency['generation'] = (generation_end_time - generation_start_time).total_seconds()
        
        if latency['generation'] > MAX_GENERATION_TIME :
            faults.append("Generation Slow")

        latency['total'] = round(time.time() - total_start_time, 3)
        
        final_output['answer'] = generated_text
        final_output['latency'] = latency
        final_output['retrieved_chunks'] = guard_output
        final_output['faults'] = faults
        final_output['confidence'] = guard_output[0]['confidence']

        return final_output