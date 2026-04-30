from django.db import models
from django.utils import timezone
from django.conf import settings
from .utils.choices import POST_STATUS_CHOICES, POST_DRAFT, TASK_TYPE_CHOICES
from .manager import PostManager, CommentManager, OTPManager


class Posts(models.Model):

    user = models.ForeignKey(                    # 👈 added
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=POST_STATUS_CHOICES, default=POST_DRAFT)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = PostManager()


class Comments(models.Model):

    user = models.ForeignKey(                    # 👈 added
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()


class OTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,  # keep flexible
        related_name='otps'
    )
    otp = models.CharField(max_length=6)
    has_used = models.BooleanField(default=False)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    objects = OTPManager()