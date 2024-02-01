"""Views for Email IMAP API"""
from rest_framework import status, generics
from rest_framework.response import Response
from core.models import ImapEmail

from utilities.command_executor import CommandExecutor
from utilities.imap_email_handler import ImapEmailHandler
from utilities.config import KEYWORD, EMAIL_CREDENTIALS
import json

class ImapEmailViewSet(generics.GenericAPIView):
    """Email Credentials View"""

    def get(self, request, *args, **kwargs):
        queryset = ImapEmail.objects.all()
        return Response(queryset.values(), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            email = EMAIL_CREDENTIALS['email']
            password = EMAIL_CREDENTIALS['password']
            imap_server = EMAIL_CREDENTIALS['imap_server']

            email_manager = ImapEmailHandler(email, password, imap_server)
            mail_id_list = email_manager.search_emails(KEYWORD, email)
            msgs_unformatted = email_manager.fetch_emails(mail_id_list)
            msgs = email_manager.process_emails(msgs_unformatted)

            for msg in msgs:
                ImapEmail.objects.create(
                    subject=msg.get('Subject', ''),
                    from_email=msg.get('From', ''),
                    timestamp=msg.get('Date', ''),
                    body=msg.get('Body', '')
                )
            
            executor = CommandExecutor()
            executor.execute_fine_tunning()
            
            return Response(msgs, status=status.HTTP_200_OK)
        
        except json.JSONDecodeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
