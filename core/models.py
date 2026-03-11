from django.db import models
from django.conf import settings
from django.utils import timezone
from .utils.choices import POST_STATUS_CHOICES, POST_DRAFT, TASK_TYPE_CHOICES
from .manager import PostManager, CommentManager, OTPManager

class Posts(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=POST_STATUS_CHOICES, default=POST_DRAFT)
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='posts'
    # )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = PostManager()


class Comments(models.Model):
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
    otp = models.CharField(max_length=6)
    has_used = models.BooleanField(default=False)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    objects = OTPManager()

    @property
    def is_expired(self):
        """True if past expired_at (computed from expired_at, not stored)."""
        if not self.expired_at:
            return False
        return timezone.now() > self.expired_at


