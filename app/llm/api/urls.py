"""URLs for Email API handler"""
from django.urls import path
from llm.api.views import LLMInferenceViewSet

urlpatterns = [
    path('llama2/', LLMInferenceViewSet.as_view(), name='llama2-inference'),
]