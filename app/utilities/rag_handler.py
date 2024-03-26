import os
import logging
import warnings
from utilities.config import HUGGINGFACE_ACCESS_TOKEN
from app.settings import INBOX_DB_CONFIG
from embedchain import App
from embedchain.loaders.postgres import PostgresLoader


os.environ["HUGGINGFACE_ACCESS_TOKEN"] = HUGGINGFACE_ACCESS_TOKEN

class RAGHandler:
    _instance = None
    
    def __new__(cls, model_config):
        if cls._instance is None:
            cls._instance = super(RAGHandler, cls).__new__(cls)
            cls._instance._rag_app = App.from_config(model_config)
        return cls._instance

    @property
    def rag_app(self):
        return self._rag_app
    
    def get_rag_response(self, question) -> str:        
        try:
            logging.info(f"Executing query: {question}")
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=FutureWarning)
                response = self.rag_app.query(question)
                logging.info(f"Response: {response} \n")
                return response
        except Exception as e:
            logging.exception("Unexpected error occurred when generating rag response.")
            return ({"detail": " An unexpected error occurred, " + str(e)}) 
        
        
    def add_source_csv(self, path):
        self.rag_app.add(path, data_type='csv')

    def add_source_docx(self, path):
        self.rag_app.add(path, data_type='docx')

    def add_postgres_source(self):
        postgres_loader = PostgresLoader(config=INBOX_DB_CONFIG)
        self.rag_app.add('SELECT * FROM core_inboxemail', data_type='postgres', loader=postgres_loader)