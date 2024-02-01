"""Views for Email IMAP API"""
from rest_framework import status, generics
from rest_framework.response import Response

from llm.api.serializers import LLMInferenceSerializer
from utilities.create_email_draft import create_email_draft
import json

class LLMInferenceViewSet(generics.GenericAPIView):
    serializer_class = LLMInferenceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            llm_response = create_email_draft(
                to_address='apacheco@arkusnexus.com',
                subject='Collaboration on Research',
                prompt=validated_data['prompt'],
            )

            return Response({
                'llm_response': llm_response,
                'message': 'LLM response generated successfully',
                }, status=status.HTTP_200_OK)
        except json.JSONDecodeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)