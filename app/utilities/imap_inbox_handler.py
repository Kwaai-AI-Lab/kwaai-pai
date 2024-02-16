from imaplib import IMAP4_SSL

from email import message_from_bytes
from email.header import decode_header
import polars as pl
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import logging
from rest_framework.response import Response
from rest_framework import status, generics
from utilities.config import MODEL_SPAM_FILTER, API_KEY_OPENAI, MODEL_TAGGING

from openai import OpenAI
import os

CLIENT = OpenAI(api_key= API_KEY_OPENAI)

class ImapInboxHandler:
    def __init__(
            self, 
            user, 
            password, 
            imap_server = 'imap.gmail.com'
        ) -> None:
        self.user = user
        self.password = password
        self.imap_server = imap_server
        self.mail = IMAP4_SSL(imap_server)
        self.mail.login(user, password)
        self.mail.select('Inbox')
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_SPAM_FILTER)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_SPAM_FILTER, from_tf=True)
        self.mail.select(mailbox='Inbox', readonly=False)
        

    def extract_email_info(self, msg_data):
        """
        This function extracts the email information from the email message.
        
        Args:
            msg_data (tuple): Tuple of email message data.
            
        Returns:
            id (str): Email message id.
            subject (str): Email message subject.
            sender (str): Email message sender.
            date (str): Email message date.
            body (str): Email message body.
            message_id (str): Email Message ID.
        """
        msg_bytes = msg_data[0][1]
        msg = message_from_bytes(msg_bytes)
        
        id = msg_data[0][0].decode().split()[0]

        subject, encoding = decode_header(msg.get('Subject', 'No Subject'))[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')

        sender, encoding = decode_header(msg.get('From', 'No Sender'))[0]
        if isinstance(sender, bytes):
            sender = sender.decode(encoding or 'utf-8')

        message_id, encoding = decode_header(msg.get('Message-ID', 'No Message ID'))[0]
        if isinstance(message_id, bytes):
            message_id = message_id.decode(encoding or 'utf-8')            

        date = msg.get('Date', 'No Date')

        body = 'No Body' 
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8').lower()
                    break
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')

        return id, subject, sender, date, body, message_id    
    
    
    def create_df_unseen_emails(self, unseen_msgs): 
        """
        This function creates a polars DataFrame of unseen emails.
        
        Args:
            unseen_msgs (list): List of unseen emails.
            
        Returns:
            df_unseen_emails (pl.DataFrame): DataFrame of unseen emails.
        """       
        data_list = []
        try:
            if not unseen_msgs:
                print("No unseen emails")
                df_unseen_emails = pl.DataFrame()
                return  df_unseen_emails 
            else:
                for msg in unseen_msgs:
                    id, subject, sender, date, body, message_id = self.extract_email_info(msg)                                       
                    data_list.append({'Id': id, 'Subject': subject, 'Sender': sender, 'Date': date, 'Body': body, 'Message-ID': message_id})
                            
                df_unseen_emails = pl.DataFrame(data_list).select(pl.all())        
                return df_unseen_emails
        except Exception as e:
            logging.exception(f"Error creating DataFrame of unseen emails:")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        
    
    def get_donot_reply_emails(self, unseen_msgs, words):
        """
        This function returns a list of ids of "do not reply emails".
        
        Args:
            unseen_msgs (list): List of unseen emails.
            WORDS (list): List of words.

        Returns:
            donot_reply_mail_ids (list): List of "do not reply emails".
        """
        
        donot_reply_mail_ids = []
        data_list = []
        
        for msg in unseen_msgs:
            id, subject, sender, _, body, message_id  = self.extract_email_info(msg)
            data_list.append({'Id': id, 'Subject': subject, 'Sender': sender, 'Body': body,'Message-ID': message_id})
           
        for email_data in data_list:
            subject_lower = email_data['Subject'].lower()
            sender_lower = email_data['Sender'].lower()
            body_lower = email_data['Body'].lower()

            if any(word in sender_lower or word in body_lower or word in subject_lower for word in words):
                donot_reply_mail_ids.append(email_data['Id'])
            
        return donot_reply_mail_ids
            
                
    def create_directories(self, new_directories):
        """
        This function extract a list of directories.
        If some directory does'nt exist, it will be created.
        
        Args:
            new_directories (list): List of new directories.
       
        """
        directories=[]
        for directory in self.mail.list()[1]:
            directories.append(directory.decode().split(' "/" ')[1])
        for new_directory in new_directories:
            if new_directory not in directories:
                self.mail.create(new_directory)


    def filter_unseen_emails(self, df_unseen_emails, donot_answer_mail_ids): 
        """
        This function rules out emails no-reply, 
        unsuscribe or potential spam, and keeps a list of clean emails.
        
        Args:
            df_unseen_emails (pl.DataFrame): DataFrame of unseen emails.
        
        Returns:
            result_list (list): List of available emails to create a draft reply.
            
        """
        try:
            df_unseen_emails = df_unseen_emails.with_columns(
                pl.concat_str(
                    df_unseen_emails['Id'],
                    df_unseen_emails['Subject'],
                    df_unseen_emails['Sender'],
                    df_unseen_emails['Date'],
                    df_unseen_emails['Body'],
                    df_unseen_emails['Message-ID'],
                    separator='||'
                ).alias('text'),
            )
            
            X_test = df_unseen_emails['text'].to_list()

            batch_encoding = self.tokenizer(X_test, truncation=True, padding=True,  return_tensors="pt")

            with torch.no_grad():
                outputs = self.model(**batch_encoding)
                predictions = F.softmax(outputs.logits, dim=1)
                labels = torch.argmax(predictions, dim=1)   

            df_final = pl.DataFrame({'text': X_test, 'label_hf': labels.tolist(), 'Id': df_unseen_emails['Id'].cast(pl.Int64)})                      
            
            df_unseen_emails = df_unseen_emails.with_columns(df_unseen_emails['Id'].cast(pl.Int64))
            donot_answer_mail_ids = list(map(int, donot_answer_mail_ids))
            
            df_no_reply = df_final.filter(pl.col('Id').is_in(donot_answer_mail_ids)) 
            
            df_no_reply = df_no_reply.with_columns(
                df_no_reply['label_hf'].replace([0], [1])
            )
            
            df_final = df_final.join(df_no_reply, on='Id', how='left').fill_null(df_final['label_hf'])            
            df_final = df_final.drop(['text_right', 'label_hf'])
            df_final = df_final.rename({'label_hf_right': 'label'})
            df_final = df_final.with_columns(df_final['Id'].cast(str)) 
            
            clean_ids = []
            clean_emails= []           
            for i in range(len(df_final)):
                if df_final['label'][i] == 0:
                    clean_emails.append(df_final['text'][i])
                    clean_ids.append(df_final['Id'][i])            

            result_list = []
            for item in clean_emails:
                parts = item.split("||")  
                id, subject, sender, date, body, message_id= parts[:6]  
                result_dict = {'Id': id , 'Subject': subject, 'From': sender, 'Date': date, 'Body': body, 'Message-ID': message_id}
                result_list.append(result_dict)

            logging.info('result_list: ',result_list)

            return result_list, df_final
        
        except pl.exceptions.PolarsError as e:            
            return [], pl.DataFrame({'error_message': [f"Empty Data Error: {e}"]})
        except ValueError as e:
            return [], pl.DataFrame({'error_message': [f"Value Error: {e}"]})
        except Exception as e:
            return [], pl.DataFrame({'error_message': [f"Unexpected Error: {e}"]})
        except pl.exceptions.ColumnNotFoundError as e:
            return [], pl.DataFrame({'error_message': [f"Unexpected Error: {e}"]})
        
    def tag_emails(self, df_final, new_directories):
            """
            This function classifies clean emails into 2 categories:
            personal and professional.
        
            Args:
                clean_emails (list): List of clean emails.
                df_final (pl.DataFrame): DataFrame of unseen emails.
                new_directories (list): List of new directories.
            """
            new_directories = [item for item in new_directories if item != 'Undefined']
            for i in range(len(df_final)):
                if df_final['label'][i] == 1:
                    self.mail.copy(df_final['Id'][i], 'Undefined')
                else:
                    completion = CLIENT.chat.completions.create(
                        model= MODEL_TAGGING,
                        messages=[
                            {"role": "system", "content": "You're a classifier email bot."},
                            {"role": "user", "content": f"Classify the purpose of the following email as either  {', '.join(map(str, new_directories))} based on its content. Please provide a clear and concise categorization without explaining the reasons for your classification. I just need 1 word,  {', '.join(map(str, new_directories))}:\n\n{df_final[i]}"}
                        ]
                    )
                    chosen_label = completion.choices[0].message.content
    
                    if chosen_label in new_directories:
                        self.mail.copy(df_final['Id'][i], chosen_label)
                    else:                        
                        logging.error(f"Unhandled label: {chosen_label}")