from transformers import AutoTokenizer
import transformers 
import torch
from utilities.config import MODEL_NAME

class LLMResponseGenerator:
    def __init__(self, model_path = MODEL_NAME):
        self.model = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            torch_dtype=torch.float32,
            device_map="auto",
        )

    def generate_response(self, input_text):
        sequences = self.pipeline(
            input_text,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            repetition_penalty=1.5,
            eos_token_id=self.tokenizer.eos_token_id,
            max_length=500,
        )

        result = ''
        for seq in sequences:
            result += seq['generated_text']
        return result
