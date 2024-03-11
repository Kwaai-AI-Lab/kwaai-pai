from celery import Celery, shared_task
from utilities.create_email_draft import create_email_draft
from utilities.get_unseen_emails import get_unseen_emails
import logging
from utilities.add_rag_source import add_rag_source_csv, add_rag_source_docx
from utilities.get_rag_response import get_rag_response
import os

celery = Celery('tasks', broker='redis://redis:6379/0')


@shared_task
def process_unseen_emails():
    try:
        path = 'utilities/'
        logging.info(f"Directory: {os.popen('ls -lha /app/utilities/').read()}")
        
        is_style_added = False

        if not is_style_added:            
            add_rag_source_docx(path + "style.docx")
            style = get_rag_response("Get the linguistic style")
            is_style_added = True

        unseen_emails = get_unseen_emails()
        if not unseen_emails:
            logging.info("No unseen emails")
            return
        else:            
            csv_files = [f for f in os.listdir(path) if f.startswith('inbox_') and f.endswith('.csv')]
            logging.info("csv_files list:", csv_files)
            if len(csv_files) > 0:                
                add_rag_source_csv(path + csv_files[-1])
            
            for unseen_email in unseen_emails:
                context = get_rag_response("Contextualize this email:"+ unseen_email['Body'])
                llm_response = create_email_draft(
                    id = unseen_email['Id'],
                    message_id = unseen_email['Message-ID'],
                    to_address = unseen_email['From'],
                    subject = 'Re: ' + unseen_email['Subject'], 
                    prompt= get_rag_response("Write an email draft that follows these guidelines:"
                                             + "\n\n1. Answer to the sender's name '" + unseen_email['From'] + "'."
                                             + "\n\n2. Maintain the tone and style following the detailed outline of her style,'"+ style + "' in your response."
                                             + "\n\n3. Directly address the content provided by the sender in the email body: '" + unseen_email['Body'] + "', and answer it."
                                             + "\n\n4. Stay relevant to the thread ID: " + unseen_email['Message-ID'] + ", and avoid mixing or referencing other email threads or conversations."
                                             + "\n\n5. Must exclude any phrases starting with 'Subject: Re:' in your response."
                                             + "\n\n6. If the context '"+ context + "' implies an invitation (e.g., to a meeting, cinema, fair, cafe, just to chat or hang out), respond appropriately and invite to check my Google Calendar by clicking on the following link: 'https://calendar.app.google/4CV2J22aYaLiWRxL8' ."
                                             + "\n\n7. Respond only to the context provided without diverging into unrelated topics."
                                             + "\n\n8. Ensure that your draft is concise, polite, and to the point, respecting the conversation's history '"+ unseen_email['Message-ID'] +"'."
                                             + "\n\n9. End the email with a respectful and personalized closing like 'Best regards' or 'Sincerely'."
                                             + "\n\n10. Do not include any disclaimers or explanatory notes within the response (e.g, Note:)."
                                             + "\n\nFocus solely on responding within the context and requirements of this specific email thread '"+ unseen_email['Message-ID'] +"'."
                                             )
                )
            
            logging.info("llm_response: %s", llm_response)
    except Exception as e:
        logging.exception(f"Error processing unseen emails: {e}")

@celery.task
def process_new_emails(emails):
    logging.info(f"Processing new emails: {emails}")

