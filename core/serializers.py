from rest_framework import serializers
from .models import Posts
from .utils.choices import POST_STATUS_CHOICES, POST_DRAFT, POST_PUBLISHED

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=POST_STATUS_CHOICES)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Posts.objects.all())
    body = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
