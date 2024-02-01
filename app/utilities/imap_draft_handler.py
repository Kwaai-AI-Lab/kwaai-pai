import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utilities.config import EMAIL_CREDENTIALS
import time

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

        message_bytes = message.as_bytes()

        _, encoded_message = self.mail.append('[Gmail]/Drafts', '', imaplib.Time2Internaldate(time.time()), message_bytes)
        
        return encoded_message
    
    def logout(self):
        self.mail.logout()
