
from embedchain import App
from utilities.config import MODEL_RAG
from utilities.rag_handler import RAGHandler
import re


def get_rag_response(question) -> str:
    rag_manager = RAGHandler(MODEL_RAG)
    response = rag_manager.get_rag_response(question)
    return response
    # pattern = r'Answer:\s*(.*?)$'
    # match = re.search(pattern, response, re.DOTALL)       
    # if match:
    #     return match.group(1)    
    # else:
    #     return "No answer found in the text."