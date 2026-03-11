from django.db import models
from .base import _soft_delete


class CommentManager(models.Manager):
    def get_all_comments(self):
        return self.filter(is_deleted=False)

    def get_comment_by_id(self, pk):
        try:
            return self.get(pk=pk, is_deleted=False)
        except self.model.DoesNotExist:
            return None

    def create_comment(self, validated_data):
        return self.create(
            body=validated_data['body'],
            post=validated_data['post']
        )

    def update_comment(self, pk, validated_data):
        instance = self.get_comment_by_id(pk)
        if instance is None:
            return None
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance

    def delete_comment(self, pk):
        instance = self.get_comment_by_id(pk)
        if instance is None:
            return False
        _soft_delete(instance)
        return True