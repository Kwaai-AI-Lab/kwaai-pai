from celery import Celery, shared_task
from utilities.create_email_draft import create_email_draft
from utilities.get_unseen_emails import get_unseen_emails
import logging
from utilities.add_rag_source import add_postgres_source
from utilities.get_rag_response import get_rag_response
import os

celery = Celery('tasks', broker='redis://redis:6379/0')

@shared_task
def process_unseen_emails():
    try:
        path = 'utilities/'
        logging.info(f"Directory: {os.popen('ls -lha /app/utilities/').read()}")
        unseen_emails = get_unseen_emails()
        if not unseen_emails:
            logging.info("No unseen emails to process.")
            return
        else:

            add_postgres_source()

            for unseen_email in unseen_emails:
                llm_response = create_email_draft(
                    id=unseen_email['Id'],
                    message_id=unseen_email['Message-ID'],
                    to_address=unseen_email['From'],
                    subject=unseen_email['Subject'], 
                    prompt=get_rag_response(
                        f"Draft a response considering the following guidelines and information:"
                        f"\n\n1. Address the sender personally, using the name {unseen_email['From']}."f"\n\n2. Answer specifically to the queries or content in the email: {unseen_email['Body']}."
                        f"\n\n3. Filter the context only in this email thread ({unseen_email['Message-ID']})."
                        f"\n\n Ensure the response is directly relevant to this thread ({unseen_email['Message-ID']}) only."
                        f"\n\n4. Avoid beginning responses with 'Subject: Re:'."
                        "\n\n5. If the email implies any form of invitation (meeting, coffee, dinner, movie), acknowledge it and suggest arranging the details through the link: 'https://calendar.app.google/4CV2J22aYaLiWRxL8'. Specify the nature of the invitation to ensure clarity."
                        f"\n\n6. Draft should be clear, polite, and concise, respecting the original email's context."
                        f"\n\n7. Finish with a signature that matches the user's usual sign-off."
                        f"\n\n8. Exclude any disclaimers, footnotes, or irrelevant details."
                        f"\n\n9. Focus on maintaining the continuity and relevance to the specific email thread."
                        f"\n\n10. Check for any attachments mentioned and acknowledge if any action is required."
                        f"\n\n11. Confirm any dates, times, or details mentioned in the email to avoid misunderstandings."
                        f"\n\n12. Ensure that the tone is appropriate for the relationship with the sender."
                        f"\n\n13. If necessary, politely decline any requests or invitations that cannot be accommodated."
                        f"\n\n14. Confirm the receipt of any important information or documents included in the email."
                        "\n\n15. Don't mix the context with other emails or threads."
                    )
                )
           
            logging.info("llm_response: %s", llm_response)
    except Exception as e:
        logging.exception(f"Error processing unseen emails: {e}")

@celery.task
def process_new_emails(emails):
    logging.info(f"Processing new emails: {emails}")