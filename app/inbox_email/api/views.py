from rest_framework import status, generics
from rest_framework.response import Response
import logging

from utilities.get_unseen_emails import get_unseen_emails


class ImapInboxView(generics.GenericAPIView):
    """   
        Handle POST requests to retrieve unseen emails from the Inbox.
        Returns:
            Response: JSON response containing a list of dictionaries 
            representing the unseen emails with the keys of:
            'Id', 'Subject', 'From', 'Date', 'Body' and 'Message-ID'.
    """
    
    def post(self, request,*args, **kwargs):
        try:
            unseen_emails = get_unseen_emails()
            return Response(unseen_emails, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when getting unseen emails.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

