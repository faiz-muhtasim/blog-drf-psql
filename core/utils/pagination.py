from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomLimitOffsetPagination(LimitOffsetPagination):

    default_limit = 10

    def get_paginated_response(self, data):
        return Response({
            "count": self.count,
            "limit": self.limit,
            "offset": self.offset,
            "results": list(data),
            "response_status": {
                "success": "true",
                "code": 200,
                "message": "message fetched successfully",
            }
        })