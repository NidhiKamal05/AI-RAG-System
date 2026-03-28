
from transformers import AutoTokenizer
from settings.config import LLM_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

CHUNK_SIZE = CHUNK_SIZE
CHUNK_OVERLAP = CHUNK_OVERLAP

class Chunk :
    def __init__(self) :
        self.tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
    
    def clean_text(self, text) :
        text = text.replace("\r", "")
        cleaned_lines = []
        for line in text.split("\n") :
            stripped_line = line.strip()
            if stripped_line :
                cleaned_lines.append(stripped_line)
        text = "\n".join(cleaned_lines)
        return text
    
    def chunk_text(self, text) :
        tokens = self.tokenizer.encode(text)
        chunks = []
        start = 0
        while start < len(tokens) :
            end = start + CHUNK_SIZE
            chunk_tokens = tokens[start : end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            start = end - CHUNK_OVERLAP
        return chunks