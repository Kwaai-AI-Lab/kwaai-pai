from rest_framework import status, generics
from rest_framework.response import Response
import logging
from utilities.get_rag_response import get_rag_response
from rag_chat.api.serializers import RagSerializer
# from utilities.embedchain import send_message
# from fastapi import APIRouter, Query, responses
# from fastapi.responses import StreamingResponse
class RAGChatView(generics.GenericAPIView):
    """  
        Handle POST
 
        Returns: rag_response
           
    """
    serializer_class = RagSerializer
 
    def post(self, request, *args, **kwargs):  
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            rag_response = get_rag_response(validated_data['prompt'])
            return Response(rag_response, status=status.HTTP_200_OK)  
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)