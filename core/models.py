from django.db import models
from django.conf import settings
from .utils.choices import POST_STATUS_CHOICES, POST_DRAFT
from .manager import PostManager

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

    def __str__(self):
        return self.title