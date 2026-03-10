from rest_framework import serializers
from .models import Posts
from .utils.choices import (
    POST_STATUS_CHOICES,
    POST_DRAFT,
    POST_PUBLISHED,
    TASK_TYPE_CHOICES,
)

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

class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, read_only=True)
    has_used = serializers.BooleanField(default=False)
    task_type = serializers.ChoiceField(choices=TASK_TYPE_CHOICES)
    created_at = serializers.DateTimeField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    expired_at = serializers.DateTimeField(read_only=True)


class OTPVerifySerializer(serializers.Serializer):
    """Payload for verifying an OTP (consume and mark as used)."""
    otp = serializers.CharField(max_length=6)
    task_type = serializers.ChoiceField(
        choices=TASK_TYPE_CHOICES,
        required=False,
    )
