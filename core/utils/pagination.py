from collections import OrderedDict, defaultdict
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.db.models import Prefetch
from ..models import Comments


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        self.offset = self.get_offset(request)

        if self.count == 0 or self.offset > self.count:
            return []

        # ✅ Prefetch only active comments, sliced queryset
        sliced_qs = queryset[self.offset:self.offset + self.limit].prefetch_related(
            Prefetch(
                'comments',                          # your related_name on Comments model
                queryset=Comments.objects.filter(is_deleted=False).only(
                    'id', 'body', 'created_at', 'post_id'
                ),
                to_attr='active_comments_list'       # stored as a plain list
            )
        )

        # ✅ Pull post fields as dicts — no loop, no manual mapping
        posts_values = list(sliced_qs.values(
            'id', 'title', 'description', 'is_deleted'
        ))

        # ✅ Build comment lookup: {post_id: [comment, ...]} — dict comprehension, no loop
        comment_map = defaultdict(list)
        # Note: we still need ONE pass to group comments — but it's a single flat comprehension
        _ = [
            comment_map[c.post_id].append(
                {'id': c.id, 'body': c.body, 'created_at': c.created_at}
            )
            for post_obj in sliced_qs
            for c in post_obj.active_comments_list
        ]

        # ✅ Attach comments to each post dict — no nested loop, just dict update
        result = [
            {**post, 'comments': comment_map[post['id']]}
            for post in posts_values
        ]

        return result

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count',   self.count),
            ('limit',   self.limit),
            ('offset',  self.offset),
            ('data',    data),
            ('response_status', {
                'success': True,
                'code':    status.HTTP_200_OK,
                'message': 'Data fetched successfully',
            }),
        ]))