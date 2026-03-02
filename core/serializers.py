from rest_framework import serializers
from .models import Posts

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=[Posts.DRAFT, Posts.PUBLISHED])