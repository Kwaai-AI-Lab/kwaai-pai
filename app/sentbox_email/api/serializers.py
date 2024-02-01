"""Email IMAP serializer"""
from rest_framework import serializers
from core.models import ImapCredentials

class ImapEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImapCredentials
        fields = '__all__'