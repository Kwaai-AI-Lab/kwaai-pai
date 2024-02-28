from rest_framework import serializers
from core.models import RagChat
 
class RagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RagChat
        fields = '__all__'
        read_only_fields = ('id',)