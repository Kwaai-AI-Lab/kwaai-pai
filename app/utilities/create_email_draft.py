"""This module creates an email draft using the LLM response model"""
from utilities.config import EMAIL_CREDENTIALS
from utilities.imap_draft_handler import ImapDraftHandler
from utilities.llm_response import stream_response_and_concatenate

def create_email_draft(    
    message_id: str,
    to_address: str,
    subject: str,
    prompt: str,
) -> str:
    """Create an email draft using llm response model"""
    draft_manager = ImapDraftHandler(
        EMAIL_CREDENTIALS['email'],
        EMAIL_CREDENTIALS['password'],
        EMAIL_CREDENTIALS['imap_server']
    )

    llm_response = stream_response_and_concatenate(prompt)


    draft_manager.login()
    draft_manager.select_drafts_mailbox()
    draft_manager.create_draft(message_id, to_address, subject, llm_response)
    draft_manager.logout()

    return llm_response