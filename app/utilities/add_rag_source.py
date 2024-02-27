import logging
import os
import warnings
from embedchain import App
from utilities.config import  MODEL_RAG, RAG_SOURCE
from utilities.rag_handler import RAGHandler


def add_rag_source() -> str:
    rag_manager = RAGHandler( MODEL_RAG)
    rag_manager.add_source()