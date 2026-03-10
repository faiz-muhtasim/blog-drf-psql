from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Comments
from core.serializers import CommentSerializer
from core.utils.pagination import CustomLimitOffsetPagination

class CommentListCreateView(APIView):
    pagination_class = CustomLimitOffsetPagination()

    def get(self, request):
        comments = Comments.objects.get_all_comments()
        paginator = self.pagination_class
        page = paginator.paginate_queryset(comments, request, view=self)
        serializer = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request):
        try:
            serializer = CommentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            comment = Comments.objects.create_comment(serializer.validated_data)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        comment = Comments.objects.get_comment_by_id(pk)
        if not comment:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CommentSerializer(comment).data)
    def put(self, request, pk):
        try:
            comment = Comments.objects.get_comment_by_id(pk)
            if not comment:
                return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CommentSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            updated_comment = Comments.objects.update_comment(comment, serializer.validated_data)
            return Response(CommentSerializer(updated_comment).data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, pk):
        try:
            comment = Comments.objects.get_comment_by_id(pk)
            if not comment:
                return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
            Comments.objects.delete_comment(comment)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)