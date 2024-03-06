from utilities.g_calendar import check_calendar_events
from celery import Celery, shared_task
from utilities.create_email_draft import create_email_draft
from utilities.get_unseen_emails import get_unseen_emails
import logging
from utilities.add_rag_source import add_rag_source
from utilities.get_rag_response import get_rag_response
import os
import datetime


celery = Celery('tasks', broker='redis://redis:6379/0')


@shared_task
def process_unseen_emails():
    try:
        
        today = datetime.datetime.now().strftime('%A %B %d of %Y at %I:%M %p')
        logging.info("Today is: ", today)     

        unseen_emails = get_unseen_emails()
        events = check_calendar_events()
        all_events = ""

        if events:
            for event in events:
                all_events += f"start: {event['start']}, end: {event['end']}, summary: {event['summary']}\n"
        else:
            all_events = "No events soon"
        
        logging.info(f"Directory: {os.popen('ls -lha /app/utilities/').read()}")
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
                date_proposed = get_rag_response('What is the date time proposed in this email? :'+ unseen_email['Body']) 
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
                                             + " \n\n" +"A good email draft keeps the tone of the email body that could be personal or professional tone."
                                             + " \n\n" +"You have to be careful to answer only on this thread id: " + unseen_email['Message-ID'] +"."
                                             + " \n\n" +"You have to be aware that today is: " + today +" and the date and time proposed is: " + date_proposed
                                             + " \n\n" + "and the next near events in your calendar are: " + all_events +"."
                                             + " \n\n" +", so if there is any conflict with my event list: " + all_events + "and the date and time proposed:" + date_proposed
                                             +  " \n\n" +"you have to answer to propose reschedule the meeting.")
                )                                                             
            logging.info("llm_response: %s", llm_response)  
    except Exception as e:
        logging.exception(f"Error processing unseen emails: {e}")

@celery.task
def process_new_emails(emails):
    logging.info(f"Processing new emails: {emails}")

