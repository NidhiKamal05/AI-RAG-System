from settings.config import MAX_ALLOWED_CHUNKS, REFUSAL_MESSAGE
from models.llm_model import LLMModel

class Generator :
    def __init__(self) :
        pass
    
    def build_context(self, guard_output) :
        docs = []

        for chunk in guard_output :
            content = f"{chunk['document']}\n(chunk_id:{chunk['metadata']['chunk_id']})"
            docs.append(content)
        
        return docs[:MAX_ALLOWED_CHUNKS]
    	
    def generation(self, query, guard_output) :
        llm = LLMModel()
        	
        context = self.build_context(guard_output)
        	
        prompt = f"""<|system|>
        You are a python expert assistant.
        Think step by step.
        Answer using only the provided context.
        If answer is not present in the provided context say {REFUSAL_MESSAGE}.
        <|user|>
        Context: {context}
        Question: {query}
        """
        	
        answer = llm.generate(prompt)
    	
        return answer if answer else REFUSAL_MESSAGE