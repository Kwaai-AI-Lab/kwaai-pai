import logging
from utilities.config import MODEL_RAG
from utilities.rag_handler import RAGHandler
import re

def get_rag_response(question) -> str:
    rag_manager = RAGHandler(MODEL_RAG)
    response = rag_manager.get_rag_response(question)
    logging.info("Raw Response: ", response) 
    pattern = r'Answer:(.*)'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        extracted_text = match.group(1).strip()
        logging.info("Extracted text: ", extracted_text)
    return extracted_text

    
    