from utilities.config import EMAIL_CREDENTIALS
from utilities.imap_email_handler import ImapEmailHandler
from utilities.imap_inbox_handler import ImapInboxHandler
import logging

DIRECTORIES = ['Personal', 'Professional', 'Education', 'Undefined']
WORDS = ['no-reply', 'unsubscribe', 'noreply','-noreply','no_reply', 'not reply']

def get_unseen_emails() -> list:
    """This function checks for unseen emails, filters them
       and tags them. Then it returns a list of dictionaries
       representing the unseen emails with the keys of:
       'Id', 'Subject', 'From', 'Date', 'Body' and 'Message-ID'.
    """
    try:
        email = EMAIL_CREDENTIALS['email']
        password = EMAIL_CREDENTIALS['password']
        imap_server = EMAIL_CREDENTIALS['imap_server']

        email_manager = ImapEmailHandler(email, password, imap_server)
        email_inbox_manager = ImapInboxHandler(email, password, imap_server)
        email_inbox_manager.create_directories(DIRECTORIES)

        unseen_mail_ids = email_manager.search_emails('UNSEEN')
        print("unseen_mail_ids =======================",unseen_mail_ids)
        msgs_unformatted = email_manager.fetch_emails(unseen_mail_ids)
        print("msgs_unformatted =======================",msgs_unformatted)
        donot_reply_mail_ids = email_inbox_manager.get_donot_reply_emails(msgs_unformatted, WORDS)
        df_unseen_emails = email_inbox_manager.create_df_unseen_emails(msgs_unformatted)

        result_list, df_final = email_inbox_manager.filter_unseen_emails(df_unseen_emails, donot_reply_mail_ids)
        print("df_final =======================",df_final)
        print("tags =======================")
        email_inbox_manager.tag_emails(df_final, DIRECTORIES)        
        print("result_list =======================",result_list)
        return result_list
    
    except Exception as e:
        logging.exception("Unexpected error occurred when checking unseen emails.")
        return ({"detail": " An unexpected error occurred, " + str(e)}) 
        