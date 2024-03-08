from utilities.config import  MODEL_RAG
from utilities.rag_handler import RAGHandler

def add_rag_source_csv(path) -> str:
    rag_manager = RAGHandler(MODEL_RAG)
    rag_manager.add_source_csv(path)

def add_rag_source_docx(path) -> str:
    rag_manager = RAGHandler(MODEL_RAG)
    rag_manager.add_source_docx(path)