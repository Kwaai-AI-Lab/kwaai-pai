from rest_framework import status, generics
from rest_framework.response import Response
import logging
from utilities.add_rag_source import add_rag_source
from utilities.config import RAG_SOURCE



#from utilities.get_unseen_emails import get_unseen_emails


class RAGAddView(generics.GenericAPIView):
    """   
        Handle POST Adds a new source to the Embedchain app.

        Returns:
            
    """
    
    def post(self, request,*args, **kwargs):
        try:
            source = add_rag_source()
            return Response(source, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

