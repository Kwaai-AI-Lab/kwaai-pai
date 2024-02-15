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
   
    
    #async def get(query: str, session_id: str = Query(None), number_documents: int = 3, citations: bool = True, stream: bool = True, model: str = "gpt-3.5-turbo-1106"):
    def post(self, request, *args, **kwargs):  
        email_string = """Subject: School Reminder - Back to Class on February 15th ### From: School Notifications <notifications@school.edu> ### Date: 2024-02-15 00:00:00-07:00 ### Body: Dear Parent/Guardian,

        This is a reminder that the new school term begins on February 15th. Please ensure that your child is prepared for the upcoming academic year.

        If you have any questions or concerns, feel free to contact the school office at notifications@school.edu or call (555) 789-0123.

        Wishing your child a successful school year!

        Sincerely,
        School Administration
        """          
        rag_response = get_rag_response("What is the date and time of the dental appointment according to the confirmation email from Dentista Mexico?")
        try:
            #generator = send_message(query, session_id, number_documents, citations, stream, model)
            return Response(rag_response, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

