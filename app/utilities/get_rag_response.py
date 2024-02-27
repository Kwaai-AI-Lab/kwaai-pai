import logging
import os
import warnings
from embedchain import App
from utilities.config import MODEL_RAG
from utilities.rag_handler import RAGHandler


def get_rag_response(question) -> str:
    rag_manager = RAGHandler(MODEL_RAG)
    response = rag_manager.get_rag_response(question)
    
    return response