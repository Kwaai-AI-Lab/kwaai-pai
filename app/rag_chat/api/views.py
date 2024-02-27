from rest_framework import status, generics
from rest_framework.response import Response
import logging
from utilities.get_rag_response import get_rag_response
# from utilities.embedchain import send_message
# from fastapi import APIRouter, Query, responses
# from fastapi.responses import StreamingResponse

class RAGChatView(generics.GenericAPIView):
    """Rag Chat View."""
    def post(self, request, *args, **kwargs):  
        # rag_response = get_rag_response("Give me the context of this email, I need to answer it: " + unseen_email)                
        rag_response = get_rag_response("Give me the context of this email, I need to answer it: ")
        try:
            return Response(rag_response, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 