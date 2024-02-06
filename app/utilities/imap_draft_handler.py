import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utilities.config import EMAIL_CREDENTIALS
import time
import base64

class ImapDraftHandler:
    def __init__(
            self, 
            email_address=EMAIL_CREDENTIALS['email'], 
            password=EMAIL_CREDENTIALS['password'],
        ):
        self.email_address = email_address
        self.password = password
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')

    def login(self):
        self.mail.login(self.email_address, self.password)

    def select_drafts_mailbox(self):
        self.mail.select('[Gmail]/Drafts')

    def create_draft(self, to_address, subject, body):
        message = MIMEMultipart()
        message['From'] = self.email_address
        message['To'] = to_address
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # thread_id = '18d67226bcd27a90'

        # request_body = {
        #     'message': {'raw': raw_string, 'threadId': thread_id}
        # }
        # #message_bytes = message.as_bytes()

        # _, encoded_message = self.mail.append('[Gmail]/Drafts', '', imaplib.Time2Internaldate(time.time()), request_body)

        message_bytes = message.as_bytes()

        _, encoded_message = self.mail.append('[Gmail]/Drafts', '', imaplib.Time2Internaldate(time.time()), message_bytes)
        
        
        return encoded_message
    
    def logout(self):
        self.mail.logout()
