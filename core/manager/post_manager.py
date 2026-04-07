from django.db import models
from .base import _soft_delete
from ..utils.choices import POST_DRAFT
from django.db.models import Q
from django.db.models import Prefetch

class PostManager(models.Manager):
    def get_all_posts(self):
        from ..models import Comments  # 👈 move import here

        return self.filter(is_deleted=False).prefetch_related(
            Prefetch(
                    'comments',
                    queryset=Comments.objects.filter(is_deleted=False),
                    to_attr='active_comments'
                )
            )

    def get_post_by_id(self, pk):
        try:
            return self.get(pk=pk, is_deleted=False)
        except self.model.DoesNotExist:
            return None

    def create_post(self, validated_data, user):          # 👈 added user param
        return self.create(
            user=user,                                     # 👈 save user
            title=validated_data['title'],
            description=validated_data['description'],
            status=validated_data.get('status', POST_DRAFT)
        )

    def update_post(self, pk, validated_data):
        instance = self.get_post_by_id(pk)
        if instance is None:
            return None
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def delete_post(self, pk):
        instance = self.get_post_by_id(pk)
        if instance is None:
            return False
        _soft_delete(instance)
        instance.comments.filter(is_deleted=False).update(is_deleted=True)
        return True

    def search_posts(self, keyword):
        from ..models import Comments  # 👈 same here

        return self.filter(
            Q(title__icontains=keyword) | Q(description__icontains=keyword),
            is_deleted=False
        ).prefetch_related(
            Prefetch(
                'comments',
                queryset=Comments.objects.filter(is_deleted=False),
                to_attr='active_comments'
            )
        )