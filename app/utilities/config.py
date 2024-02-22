import os

MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
MODEL_SPAM_FILTER = "NotShrirang/albert-spam-filter"
MODEL_TAGGING = "gpt-3.5-turbo"

HUGGINGFACE_ACCESS_TOKEN = "hf_****"
MODEL_RAG = "utilities/mistral.yaml"
RAG_SOURCE = "utilities/Inbox.csv"

EMAILS_DATA_SET_PATH = './sent_box_emails.csv'
KEYWORD = 'FROM'

EMAIL_CREDENTIALS = {
    "email": os.environ.get("IMAP_EMAIL"),
    "password": os.environ.get("IMAP_PASSWORD"),
    "imap_server": os.environ.get("IMAP_HOST"),
}

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

EC_APP_CONFIG = {
    "app": {
        "config": {
            "id": "embedchain-demo-app",
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-3.5-turbo-1106",
        }
    }
}


