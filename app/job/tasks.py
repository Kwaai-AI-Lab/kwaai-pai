from utilities.g_calendar import check_calendar_events
from celery import Celery, shared_task
from utilities.create_email_draft import create_email_draft
from utilities.get_unseen_emails import get_unseen_emails
import logging
from utilities.add_rag_source import add_rag_source
from utilities.get_rag_response import get_rag_response
import os
import webbrowser
urL='https://www.google.com'


celery = Celery('tasks', broker='redis://redis:6379/0')
# chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
# webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
# webbrowser.get('chrome').open_new_tab(urL)

@shared_task
def process_unseen_emails():
    try:
        unseen_emails = get_unseen_emails()
        start_e, end_e, summary = check_calendar_events()
        # start_e= '2024-03-08T9:30:00-07:00'
        # end_e= '2024-03-08T10:30:00-07:00'
        summary= 'Kwaai backend meeting'
        logging.info(f"Directory: {os.popen('ls -lha /app/utilities/').read()}")
        logging.info(f"Calendar events: {start_e}, {end_e}, {summary}")
        if not unseen_emails:
            logging.info("No unseen emails")
            return            
        else:                      
            path = 'utilities/'             
            csv_files = [f for f in os.listdir(path) if f.startswith('inbox_') and f.endswith('.csv')]                         
            logging.info("csv_files list:", csv_files)            
            if len(csv_files) > 0:            
                add_rag_source(path + csv_files[-1])                      
            for unseen_email in unseen_emails:
                llm_response = create_email_draft(
                    message_id = unseen_email['Message-ID'],
                    to_address = unseen_email['From'],                
                    subject = 'Re: ' + unseen_email['Subject'],
                    prompt= get_rag_response("Your goal is to write a good draft of an email that:"
                                             + " \n\n" +"it is written in the same tone as if you were Yoda from Star Wars" 
                                             + " \n\n" +",it answers to the sender's email: " + unseen_email['From']
                                             + " \n\n" +",it answers only to the following thread id:"  + unseen_email['Message-ID'] 
                                             + " \n\n" +",it answers to the following email body:"  + unseen_email['Body']                                            
                                             + " \n\n" +",it does not include 'Subject:' phrase in the response." 
                                             + " \n\n" +"A good email draft keeps the tone of the email body that could be personal or professional tone"
                                             + " \n\n" +"You have to be careful to answer only on this thread id: " + unseen_email['Message-ID']
                                             + " \n\n" +"if there is any conflict with the event: " + start_e + " and " + end_e + "and the date and time proposed in the email body" +
                                               " \n\n" +"you have to answer to the email with the following message: " 
                                                       +"I am sorry, I cannot attend the meeting at the proposed time. I have another meeting at the same time. Can we reschedule the meeting?")
                                             )                
            logging.info("llm_response: %s", llm_response)  
    except Exception as e:
        logging.exception(f"Error processing unseen emails: {e}")

@celery.task
def process_new_emails(emails):
    logging.info(f"Processing new emails: {emails}")

