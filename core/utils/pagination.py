from collections import OrderedDict, defaultdict
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        self.offset = self.get_offset(request)

        if self.count == 0 or self.offset > self.count:
            return []

        # ✅ Evaluate once — DB hit happens here, prefetch cache is populated
        sliced_qs = list(queryset[self.offset:self.offset + self.limit])

        # ✅ Build post dicts from model instances (no extra query)
        posts_values = [
            {'id': p.id, 'title': p.title, 'description': p.description, 'status': p.status}
            for p in sliced_qs
        ]

        # ✅ Build comment lookup from already-prefetched active_comments (no extra query)
        comment_map = defaultdict(list)
        _ = [
            comment_map[post_obj.id].append(
                {'id': c.id, 'body': c.body, 'created_at': c.created_at}
            )
            for post_obj in sliced_qs
            for c in post_obj.active_comments  # 👈 to_attr set in manager.py
        ]

        # ✅ Merge comments into post dicts
        return [
            {**post, 'comments': comment_map[post['id']]}
            for post in posts_values
        ]

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