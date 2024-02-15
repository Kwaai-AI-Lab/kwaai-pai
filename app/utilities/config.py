MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
EMAILS_DATA_SET_PATH = './sent_box_emails.csv'
KEYWORD = 'FROM'

EMAIL_CREDENTIALS = {
    "email": "your_email",
    "password": "your_password",
    "imap_server": "imap.gmail.com",
}

MODEL_SPAM_FILTER = "NotShrirang/albert-spam-filter"
API_KEY_OPENAI = "sk-****"
MODEL_TAGGING = "gpt-3.5-turbo"

HUGGINGFACE_ACCESS_TOKEN = "hf-***"
MODEL_RAG = "utilities/mistral.yaml"
RAG_SOURCE = "utilities/emails.csv"

# App config using OpenAI gpt-3.5-turbo-1106 as LLM
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

# Uncomment this configuration to use Mistral as LLM
# EC_APP_CONFIG = {
#     "app": {
#         "config": {
#             "name": "embedchain-opensource-app"
#         }
#     },
#     "llm": {
#         "provider": "huggingface",
#         "config": {
#             "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
#             "temperature": 0.1,
#             "max_tokens": 250,
#             "top_p": 0.1
#         }
#     },
#     "embedder": {
#         "provider": "huggingface",
#         "config": {
#             "model": "sentence-transformers/all-mpnet-base-v2"
#         }
#     }
# }
