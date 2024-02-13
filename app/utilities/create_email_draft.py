"""This module creates an email draft using the LLM response model"""
from utilities.config import EMAIL_CREDENTIALS, MODEL_NAME
from utilities.imap_draft_handler import ImapDraftHandler
from utilities.llm_response_generator import LLMResponseGenerator

def create_email_draft(    
    message_id: str,
    to_address: str,
    subject: str,
    prompt: str,
) -> str:
    """Create an email draft using llm response model"""
    #llm = LLMResponseGenerator(model_path=MODEL_NAME)
    draft_manager = ImapDraftHandler(
        EMAIL_CREDENTIALS['email'],
        EMAIL_CREDENTIALS['password'],
        EMAIL_CREDENTIALS['imap_server']
    )

    #llm_response = llm.generate_response(prompt)

    draft_manager.login()
    draft_manager.select_drafts_mailbox()
    llm_response = draft_manager.create_draft(message_id, to_address, subject, prompt)
    draft_manager.logout()

    return llm_response