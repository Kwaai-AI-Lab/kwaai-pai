from celery import Celery, shared_task
from utilities.create_email_draft import create_email_draft
from utilities.get_unseen_emails import get_unseen_emails
import logging

celery = Celery('tasks', broker='redis://redis:6379/0')

@shared_task
def process_unseen_emails():
    try:
        unseen_emails = get_unseen_emails()

        if not unseen_emails:
            logging.info("No unseen emails")
            return

        for unseen_email in unseen_emails:
            
            llm_response = create_email_draft(
                message_id = unseen_email['Message-ID'],
                to_address = unseen_email['From'],                
                subject = 'Re: ' + unseen_email['Subject'],
                prompt= "Write an email to the following message: " + unseen_email['Body']
            )
        logging.info("llm_response: %s", llm_response)

    except Exception as e:
        logging.exception(f"Error processing unseen emails: {e}")

@celery.task
def process_new_emails(emails):
    logging.info(f"Processing new emails: {emails}")