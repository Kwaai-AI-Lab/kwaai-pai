from rest_framework import status, generics
from rest_framework.response import Response
import logging
from utilities.add_rag_source import add_rag_source_csv
import os

class RAGAddView(generics.GenericAPIView):
    """   
        Handle POST Adds a new source to the Embedchain app.
                            
    """
    
    def post(self, request,*args, **kwargs):
        try:
            path = 'utilities/'
            csv_files = [f for f in os.listdir(path) if f.startswith('inbox_') and f.endswith('.csv')]           

            if len(csv_files) > 0:
                 source =add_rag_source_csv(path + csv_files[-1])
            return Response(source, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

