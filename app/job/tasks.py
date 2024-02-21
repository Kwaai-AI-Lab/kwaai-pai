from celery import Celery, shared_task
from utilities.create_email_draft import create_email_draft
from utilities.get_unseen_emails import get_unseen_emails
import logging
from utilities.add_rag_source import add_rag_source
from utilities.get_rag_response import get_rag_response

celery = Celery('tasks', broker='redis://redis:6379/0')

@shared_task
def process_unseen_emails():
    try:
        unseen_emails = get_unseen_emails()

        
        if not unseen_emails:
            logging.info("No unseen emails")
            return
            
        else:
            # add_rag_source()
            for unseen_email in unseen_emails:
                rag_response_context = get_rag_response("Give me the context of this email, I need to answer it: " + unseen_email['Body'])                
                llm_response = create_email_draft(
                    message_id = unseen_email['Message-ID'],
                    to_address = unseen_email['From'],                
                    subject = 'Re: ' + unseen_email['Subject'],
                    prompt= get_rag_response("Write a draft email to reply the following email body: " + unseen_email['Body'] + " \n\n" + "using this context: " + rag_response_context)
                )
            logging.info("llm_response: %s", llm_response)

    except Exception as e:
        logging.exception(f"Error processing unseen emails: {e}")

@celery.task
def process_new_emails(emails):
    logging.info(f"Processing new emails: {emails}")