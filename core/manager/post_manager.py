from django.db import models
from .base import _soft_delete
from ..utils.choices import POST_DRAFT
from django.db.models import Q
from django.db.models import Prefetch

class PostManager(models.Manager):
    def get_posts(self, keyword=None):
        from ..models import Comments
        queryset = self.filter(is_deleted=False)
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )
        return queryset.select_related('user').prefetch_related(  # 👈 post author
            Prefetch(
                'comments',
                queryset=Comments.objects.filter(is_deleted=False)
                .select_related('user'),  # 👈 comment authors
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
