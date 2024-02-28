from rest_framework import status, generics
from rest_framework.response import Response
import logging
from utilities.add_rag_source import add_rag_source
import os


#from utilities.get_unseen_emails import get_unseen_emails


class RAGAddView(generics.GenericAPIView):
    """   
        Handle POST Adds a new source to the Embedchain app.

        Returns:
            
    """
    
    def post(self, request,*args, **kwargs):
        try:
            path = 'utilities/'
            csv_files = [f for f in os.listdir(path) if f.startswith('inbox_') and f.endswith('.csv')]
            print("csv_files::::::", csv_files)
            source =add_rag_source(path + csv_files[-1])
            # source = add_rag_source('utilities/inbox_2024-02-27_23-39-35.csv')
            return Response(source, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

