from rest_framework import status, generics
from rest_framework.response import Response
import logging
from utilities.get_rag_response import get_rag_response
# from utilities.embedchain import send_message
# from fastapi import APIRouter, Query, responses
# from fastapi.responses import StreamingResponse
class RAGChatView(generics.GenericAPIView):
    """   
        Handle POST

        Returns: rag_response
            
    """
    def post(self, request, *args, **kwargs): 
        unseen_email = "hello msc-it students,\r\n\r\n   we are planning to have a 1-hour lecture for each of the sections of it\r\n581 at the same time starting next week.\r\n\r\n   please select one of the following:\r\n   a)  tuesday  12 - 12:50 pm\r\n   b)  tuesday 1 - 1:50 pm\r\n   c) either of the above\r\n\r\n the 4-hour lab sections will be removed from the academic calendar. since\r\nit is an individual project course, each student will select their\r\nweekly meeting with their respective instructor.\r\n\r\n     for this week, the class will run based on the present schedule.\r\n\r\n     please let us know or talk to your supervisor if you need any\r\nadditional information.\r\n\r\n     the due date for responding to this email is *tomorrow, at 4 pm.*\r\n\r\nbest regards,\r\nana\r\n"
        rag_response = get_rag_response("Give me the context of this email, I need to answer it: " + unseen_email)                
        try:
            return Response(rag_response, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

