from settings.config import  MAX_ALLOWED_CHUNKS, REFUSAL_MESSAGE
# from models.llm_model import LLMModel

class Generator :
    def __init__(self) :
        pass
    
    def build_context(self, guard_output) :
        docs = []

        for chunk in guard_output :
            content = f"{chunk['document']}\nSource:{chunk['metadata']['source']}(chunk_id:{chunk['metadata']['chunk_id']})"
            docs.append(content)
        
        return docs[:MAX_ALLOWED_CHUNKS]

    def generation_by_groq(self, query, guard_output, model) :
        context = self.build_context(guard_output)
        
        prompt = ("\nYou are a Python Assistant. Answer using only provided context.",
                  "Cite source file and chunk id for each used file at the end (e.g. [FILE: filename.pdf | CHUNKID: 1])",
                  f"If answer is not present within the context, say {REFUSAL_MESSAGE}",
                  "Do not use internal knowledge"
                )
                
        system_prompt = '\n'.join(str(x) for x in prompt)
        print(f"System - {system_prompt}")
        
        messages = [
          {'role': 'system', 'content': system_prompt},
          {'role': 'user', 'content': f'\nContext:\n{context}\n\nQuery:\n{query}'},
          {'role': 'assistant', 'content': ''}
        ]		
        print(f"Prompt - {messages}")
        
        raw_output = model.generate_with_groq(messages)
        print(f"[GROQ_ANSWER] -> {raw_output}")
        
        return raw_output
    	
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