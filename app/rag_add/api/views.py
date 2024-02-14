from rest_framework import status, generics
from rest_framework.response import Response
import logging

#from utilities.get_unseen_emails import get_unseen_emails


class RAGAddView(generics.GenericAPIView):
    """   
        Handle POST 

        Returns:
            
    """
    
    def post(self, request,*args, **kwargs):
        try:
            return Response('rag-add view', status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

