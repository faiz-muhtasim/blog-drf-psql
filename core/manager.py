from django.contrib.auth import get_user_model
from django.db import models
from .utils.choices import POST_STATUS_CHOICES, POST_DRAFT


def _soft_delete(instance):
    """Mark an instance as deleted (soft delete)."""
    instance.is_deleted = True
    instance.save()


class PostManager(models.Manager):
    def get_all_posts(self):
        return self.filter(is_deleted=False)

    def get_post_by_id(self, pk):
        try:
            return self.get(pk=pk, is_deleted=False)
        except self.model.DoesNotExist:
            return None
    def create_post(self, validated_data):
        """
        Create a new post with the given validated data and user.
        If no user is provided or user is anonymous, assign the first superuser.
        """
        # if not user or user.is_anonymous:
        #     user = User.objects.filter(is_superuser=True).first()
        return self.create(
            # created_by=user,
            title=validated_data['title'],
            description=validated_data['description'],
            status=validated_data.get('status', POST_DRAFT)
        )

    @staticmethod
    def update_post(instance, validated_data):
        """
        Update an existing post with validated data.
        Only updates fields provided in validated_data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
    @staticmethod
    def delete_post(instance):
        _soft_delete(instance)

#==================================================
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
    @staticmethod
    def update_comment(instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
    @staticmethod
    def delete_comment(instance):
        _soft_delete(instance)
