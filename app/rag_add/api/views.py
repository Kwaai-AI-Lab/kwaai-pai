from rest_framework import status, generics
from rest_framework.response import Response
import logging
from utilities.add_rag_source import add_postgres_source

class RAGAddView(generics.GenericAPIView):
    """   
        Handle POST Adds a new source to the Embedchain app.
                            
    """
    
    def post(self, request,*args, **kwargs):
        try:
            source = add_postgres_source()
            return Response(source, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

