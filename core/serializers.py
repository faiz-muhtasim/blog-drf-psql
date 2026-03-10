from rest_framework import serializers
from .models import Posts
from .utils.choices import (
    POST_STATUS_CHOICES,
    TASK_TYPE_CHOICES,
)

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=POST_STATUS_CHOICES)

class CommentSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Posts.objects.all()) #thik kora lagbe
    body = serializers.CharField()

class OTPSerializer(serializers.Serializer):
    task_type = serializers.ChoiceField(choices=TASK_TYPE_CHOICES)

class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    task_type = serializers.ChoiceField(
        choices=TASK_TYPE_CHOICES,
        required=False,
    )
