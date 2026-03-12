from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomLimitOffsetPagination(LimitOffsetPagination):

    default_limit = 10

    def get_paginated_response(self, data):
        return Response({
            "count": self.count,
            "limit": self.limit,
            "offset": self.offset,
            "data": list(data),
            "response_status": {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Data fetched successfully",
            }
        })