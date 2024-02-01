"""URLs for Email API handler"""
from django.urls import path
from inbox_email.api.views import ImapInboxView

urlpatterns = [
    path('', ImapInboxView.as_view(), name='email-credentials'),
]