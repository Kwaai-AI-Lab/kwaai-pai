from utilities.config import EMAIL_CREDENTIALS, DIRECTORIES, WORDS
from utilities.imap_email_handler import ImapEmailHandler
from utilities.imap_inbox_handler import ImapInboxHandler
import json

def check_unseen_emails() -> list:
    """Check unseen emails"""
    try:
        email = EMAIL_CREDENTIALS['email']
        password = EMAIL_CREDENTIALS['password']
        imap_server = EMAIL_CREDENTIALS['imap_server']

        email_manager = ImapEmailHandler(email, password, imap_server)
        email_inbox_manager = ImapInboxHandler(email, password, imap_server)
        email_inbox_manager.create_directories(DIRECTORIES)

        unseen_mail_id_list = email_manager.search_emails('UNSEEN')
        msgs_unformatted = email_manager.fetch_emails(unseen_mail_id_list)

        donot_answer_mail_id_list = email_inbox_manager.get_donot_reply_emails(msgs_unformatted, WORDS)
        df_unseen_emails = email_inbox_manager.create_df_unseen_emails(msgs_unformatted)

        result_list, df_final = email_inbox_manager.filter_unseen_emails(df_unseen_emails, donot_answer_mail_id_list)

        email_inbox_manager.tag_emails(df_final, DIRECTORIES)
        
        return result_list
    except json.JSONDecodeError as e:
        return {'error': str(e)}