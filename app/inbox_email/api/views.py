"""Views for Email IMAP API"""
from rest_framework import status, generics
from rest_framework.response import Response

from utilities.check_unseen_emails import check_unseen_emails
import json

class ImapInboxView(generics.GenericAPIView):
    """Inbox emails View"""
    
    def post(self, request,*args, **kwargs):
        try:
            unseen_emails = check_unseen_emails()
            #email_inbox_manager.tag_emails(df_final_left, DIRECTORIES)

            return Response(unseen_emails, status=status.HTTP_200_OK)        
        except json.JSONDecodeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
