"""Email IMAP serializer"""
from rest_framework import serializers
from core.models import LLMResponse

class LLMInferenceSerializer(serializers.ModelSerializer):
    """Serializer for the LLMResponse object"""
    class Meta:
        model = LLMResponse
        fields = '__all__'
        read_only_fields = ('id',)