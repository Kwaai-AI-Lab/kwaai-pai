from utilities.config import  MODEL_RAG
from utilities.rag_handler import RAGHandler



def add_rag_source(path) -> str:
    rag_manager = RAGHandler(MODEL_RAG)
    rag_manager.add_source_csv(path)