from celery import Celery, shared_task
from utilities.create_email_draft import create_email_draft
from utilities.check_unseen_emails import check_unseen_emails

celery = Celery('tasks', broker='redis://redis:6379/0')

@shared_task
def process_unseen_emails():
    try:
        unseen_emails = check_unseen_emails()

        if not unseen_emails:
            print("No unseen emails")
            return

        for unseen_email in unseen_emails:
            llm_response = create_email_draft(
                to_address=unseen_emails['From'],                
                subject='Re: ' + unseen_email['Subject'],
                prompt="Write an email to the following message: " + unseen_email['Body']
            )
            print(llm_response)

    except Exception as e:
        print(f"Error processing unseen emails: {e}")

@celery.task
def process_new_emails(emails):
    print(f"Processing new emails: {emails}")