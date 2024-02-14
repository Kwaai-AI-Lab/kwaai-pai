from rest_framework import status, generics
from rest_framework.response import Response
import logging
# from utilities.embedchain import send_message
# from fastapi import APIRouter, Query, responses
# from fastapi.responses import StreamingResponse
class RAGChatView(generics.GenericAPIView):
    """   
        Handle GET 

        Returns:
            
    """
    
    #async def get(query: str, session_id: str = Query(None), number_documents: int = 3, citations: bool = True, stream: bool = True, model: str = "gpt-3.5-turbo-1106"):
    def get(self, request, *args, **kwargs):    
   
        try:
            #generator = send_message(query, session_id, number_documents, citations, stream, model)
            return Response('rag-chat view', status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

