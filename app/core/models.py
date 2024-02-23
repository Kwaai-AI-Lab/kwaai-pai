from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

    
class ImapCredentials(models.Model):
    """Email Credentials model."""
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=255)
    imap_server = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    

class ImapEmail(models.Model):
    """Email model."""
    subject = models.CharField(max_length=255)
    from_email = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject
    
class LLMResponse(models.Model):
    """LLM Response model."""
    prompt = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.response
    
class InboxEmail(models.Model):
    """Inbox Email model."""
    id = models.CharField(max_length=255, primary_key=True)
    subject = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    body = models.TextField()
    message_id = models.CharField(max_length=255)

    def __str__(self):
        return self.id