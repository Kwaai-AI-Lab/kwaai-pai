import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utilities.config import EMAIL_CREDENTIALS
import time

IMAP_LIST_COMMAND = '[Gmail]/Drafts'
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
        self.mail.select(IMAP_LIST_COMMAND)

    def create_draft(self, id, to_address, subject, body):
        message = MIMEMultipart()
        message['From'] = self.email_address
        message['To'] = to_address
        message['Subject'] = subject
        message['In-Reply-To'] = id

        message.attach(MIMEText(body, 'plain'))
       
        message_bytes = message.as_bytes()

        _, encoded_message = self.mail.append(IMAP_LIST_COMMAND, '', imaplib.Time2Internaldate(time.time()), message_bytes)
        
        return encoded_message
    
    def logout(self):
        self.mail.logout()
