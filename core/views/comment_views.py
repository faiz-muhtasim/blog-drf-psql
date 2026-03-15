from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Comments
from core.serializers import CommentSerializer
from core.utils.pagination import CustomLimitOffsetPagination
from core.utils.response import success_response, error_response


class CommentListCreateView(APIView):

    pagination_class = CustomLimitOffsetPagination()

    def get(self, request):
        comments = Comments.objects.get_all_comments().values()
        paginator = self.pagination_class
        page = paginator.paginate_queryset(comments, request, view=self)
        return paginator.get_paginated_response(page)

    def post(self, request):
        try:
            serializer = CommentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(error_response(serializer.errors, "Validation error", 400), status=status.HTTP_400_BAD_REQUEST)
            comment = Comments.objects.create_comment(serializer.validated_data)
            return Response(success_response(CommentSerializer(comment).data, "Comment created successfully", 201), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(error_response(message=str(e), code=500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentRetrieveUpdateDeleteView(APIView):

    def get(self, request, pk):
        comment = Comments.objects.get_comment_by_id(pk) # use manager, not .filter()
        if not comment:
            return Response(error_response(message="Comment not found", code=404), status=status.HTTP_404_NOT_FOUND)
        return Response(success_response(CommentSerializer(comment).data, "Comment fetched successfully", include_data=True),
                        status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            serializer = CommentSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(error_response(serializer.errors, "Validation error", 400), status=status.HTTP_400_BAD_REQUEST)
            updated_comment = Comments.objects.update_comment(pk, serializer.validated_data)
            if not updated_comment:
                return Response(error_response(message="Comment not found", code=404), status=status.HTTP_404_NOT_FOUND)
            return Response(success_response(CommentSerializer(updated_comment).data, "Comment updated successfully"), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(error_response(message=str(e), code=500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            deleted = Comments.objects.delete_comment(pk)
            if not deleted:
                return Response(error_response(message="Comment not found", code=404), status=status.HTTP_404_NOT_FOUND)
            return Response(success_response(message="Comment deleted successfully", code=204), status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(error_response(message=str(e), code=500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)