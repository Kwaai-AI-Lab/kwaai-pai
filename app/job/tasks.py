from celery import Celery, shared_task
from utilities.create_email_draft import create_email_draft
from utilities.get_unseen_emails import get_unseen_emails
import logging
from utilities.add_rag_source import add_rag_source_csv, add_rag_source_docx
from utilities.get_rag_response import get_rag_response
import os
from utilities.config import MODEL_SPAM_FILTER, OPENAI_API_KEY, MODEL_TAGGING

from openai import OpenAI

CLIENT = OpenAI(api_key= OPENAI_API_KEY)
celery = Celery('tasks', broker='redis://redis:6379/0')


@shared_task
def process_unseen_emails():
    try:
        path = 'utilities/'
        logging.info(f"Directory: {os.popen('ls -lha /app/utilities/').read()}")

        # Ensure stylistic guidelines are set up and retrieved only once.
        if 'style' not in globals():
            global style
            add_rag_source_docx(path + "style.docx")
            style = get_rag_response("Extract the linguistic style guidelines.")
        
        # Retrieve unseen emails and check for new content.
        unseen_emails = get_unseen_emails()
        if not unseen_emails:
            logging.info("No unseen emails to process.")
            return
        else:
            # Update the context with the most recent emails for accuracy.
            csv_files = [f for f in os.listdir(path) if f.startswith('inbox_') and f.endswith('.csv')]
            logging.info(f"List of CSV files: {csv_files}")
            if csv_files:
                latest_csv = sorted(csv_files)[-1]  # Ensure the latest file is used.
                add_rag_source_csv(path + latest_csv)

            for unseen_email in unseen_emails:
                # Process each email individually for context and content.
                email_contextualization = get_rag_response(f"Provide context and summary for this email: {unseen_email['Body']}")

                # Check if the email implies a meeting or invitation.
                is_meeting_response = CLIENT.chat.completions.create(
                        model=MODEL_TAGGING,
                        messages=[
                            {"role": "system", "content": "You're a meeting identification assistant."},
                            {"role": "user", "content": f"Decide if this email content implies a meeting invitation: {unseen_email['Body']}"}
                        ]
                )
                meeting_decision = is_meeting_response.choices[0].message.content
                logging.info(f"Meeting decision: {meeting_decision}")

                llm_response = create_email_draft(
                    id=unseen_email['Id'],
                    message_id=unseen_email['Message-ID'],
                    to_address=unseen_email['From'],
                    subject=unseen_email['Subject'], 
                    prompt=get_rag_response(
                        f"Draft a response considering the following guidelines and information:"
                        f"\n\n1. Address the sender personally, using the name {unseen_email['From']}."
                        f"\n\n2. Apply the provided stylistic guidelines: {style}."
                        f"\n\n3. Answer specifically to the queries or content in the email: {unseen_email['Body']}."
                        f"\n\n4. Filter the context only in this email thread ({unseen_email['Message-ID']})."
                        f"\n\n Ensure the response is directly relevant to this thread ({unseen_email['Message-ID']}) only."
                        f"\n\n5. Avoid beginning responses with 'Subject: Re:'."
                        "\n\n6. If the email implies any form of invitation (meeting, coffee, dinner, movie), acknowledge it and suggest arranging the details through the link: 'https://calendar.app.google/4CV2J22aYaLiWRxL8'. Specify the nature of the invitation to ensure clarity."
                        f"\n\n7. Draft should be clear, polite, and concise, respecting the original email's context."
                        f"\n\n8. Finish with a signature that matches the user's usual sign-off."
                        f"\n\n9. Exclude any disclaimers, footnotes, or irrelevant details."
                        f"\n\n10. Focus on maintaining the continuity and relevance to the specific email thread."
                        f"\n\n11. Check for any attachments mentioned and acknowledge if any action is required."
                        f"\n\n12. Confirm any dates, times, or details mentioned in the email to avoid misunderstandings."
                        f"\n\n13. Ensure that the tone is appropriate for the relationship with the sender."
                        f"\n\n14. If necessary, politely decline any requests or invitations that cannot be accommodated."
                        f"\n\n15. Confirm the receipt of any important information or documents included in the email."
                        "\n\n16. Don't mix the context with other emails or threads."
                    )
                )
           
            logging.info("llm_response: %s", llm_response)
    except Exception as e:
        logging.exception(f"Error processing unseen emails: {e}")

@celery.task
def process_new_emails(emails):
    logging.info(f"Processing new emails: {emails}")