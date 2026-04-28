from groq import Groq
from dotenv import load_dotenv
from settings.config import TEMPERATURE, REFUSAL_MESSAGE, GROQ_MODEL, MAX_RETRIES
import os
import time
import random

load_dotenv()

class GroqGenerator :
    def __init__(self) :
        # api_key=None
        # if not api_key :
        api_key=os.getenv("GROQ_API_KEY")
        print(f"[Generation-init]key={api_key}")
        self.client = Groq(api_key=api_key)
        self.model = GROQ_MODEL
        self.temperature = TEMPERATURE
    
    def generate_with_groq(self, messages: list[dict])->str :
        max_retries = MAX_RETRIES
        retry_delay = 2
        backoff_factor = 2
        print(f"[Generation]key={os.getenv("GROQ_API_KEY")}")
        for attempt in range(max_retries) :
          try :
            chat_completion = self.client.chat.completions.create(messages = messages, model = self.model, temperature = self.temperature)
            return chat_completion.choices[0].message.content
          except Exception as e :
            if attempt == max_retries - 1 :
              print(f"[GROQ ERROR] Final attempt failed: {e}")
              return "Sorry, we are unable to process request at this moment."
          
          sleep_time = (retry_delay * (backoff_factor ** attempt)) + random.uniform(0, 1)
          print(f"[GENERATION] Attempt {attempt + 1} failed. Retrying in {sleep_time: .2f}s...")
          time.sleep(sleep_time)
        
        return "[GENERATION][Total Attempt: {attempt + 1}] Sorry, we are unable to process request at this moment."