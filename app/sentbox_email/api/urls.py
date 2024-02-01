"""URLs for Email API handler"""
from django.urls import path
from sentbox_email.api.views import ImapEmailViewSet

urlpatterns = [
    path('', ImapEmailViewSet.as_view(), name='email-credentials'),
]