from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from settings.config import LLM_MODEL, MAX_NEW_TOKENS, TEMPERATURE, DO_SAMPLE, REPETITION_PENALTY, MAX_TIME

class LLMModel :
    def __init__(self) :
        pass

    def generate(self, prompt) :
        tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
		
        model = AutoModelForCausalLM.from_pretrained(LLM_MODEL, dtype = torch.float32)
        model.to("cpu")
        model.eval()
        
        inputs = tokenizer(prompt, return_tensors = "pt", truncation = True)
        with torch.no_grad() :
            outputs = model.generate(**inputs, max_new_tokens = MAX_NEW_TOKENS, temperature = TEMPERATURE, do_sample = DO_SAMPLE, repetition_penalty = REPETITION_PENALTY, max_time = MAX_TIME)
        
        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        generated_text = tokenizer.decode(generated_tokens, skip_special_tokens = True)
        
        return generated_text