from collections import OrderedDict, defaultdict
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


def format_post(post_obj, comments=None):
    data = {
        'id': post_obj.id,
        'title': post_obj.title,
        'description': post_obj.description,
        'status': post_obj.status,
    }
    if comments is not None:
        data['comments'] = comments
    return data


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

        # ✅ Build comment lookup from already-prefetched active_comments (no extra query)
        comment_map = defaultdict(list)
        for post_obj in sliced_qs:
            for c in post_obj.active_comments:
                comment_map[post_obj.id].append(
                    {'id': c.id, 'body': c.body, 'created_at': c.created_at}
                )

        # ✅ Build post dicts using shared helper
        return [
            format_post(p, comments=comment_map[p.id])
            for p in sliced_qs
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