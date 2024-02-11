from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model_name = "meta-llama/Llama-2-7b-chat-hf"
adapter_model_name = "./checkpoints/checkpoint-100" 

model = AutoModelForCausalLM.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(model, adapter_model_name)

tokenizer = AutoTokenizer.from_pretrained(base_model_name)

model = model.merge_and_unload()
model.save_pretrained("merged_adapters")
tokenizer.save_pretrained("merged_adapters")