import os

MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
MODEL_SPAM_FILTER = "NotShrirang/albert-spam-filter"
MODEL_TAGGING = "gpt-3.5-turbo"
MODEL_RAG = "utilities/mistral.yaml"
RAG_SOURCE = "utilities/emails.csv"


EMAILS_DATA_SET_PATH = './sent_box_emails.csv'
KEYWORD = 'FROM'

EMAIL_CREDENTIALS = {
    "email": "yoda.kwaai.test@gmail.com",
    "password": "nntv eeug lzpn zmeo",
    "imap_server": "imap.gmail.com",
}

OPENAI_API_KEY = "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"
HUGGINGFACE_ACCESS_TOKEN = "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"

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