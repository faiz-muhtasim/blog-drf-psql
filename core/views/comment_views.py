from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Comments
from core.serializers import CommentSerializer
from core.utils.pagination import CustomLimitOffsetPagination
from core.utils.formatter import format_comment
from core.utils.response import success_response, error_response
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging

logger = logging.getLogger(__name__)


class CommentListCreateView(APIView):

    pagination_class = CustomLimitOffsetPagination()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        try:
            comments = Comments.objects.get_all_comments()
            page = self.pagination_class.paginate_queryset(comments, request, view=self)
            return self.pagination_class.get_paginated_response(page)

        except Exception as e:
            logger.error(f"Error fetching comments: {e}")
            return Response(error_response(message="Something went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = CommentSerializer(data=request.data)
            if not serializer.is_valid():
                logger.warning(f"Comment creation validation failed: {serializer.errors}")
                return Response(error_response("Information is invalid", status.HTTP_400_BAD_REQUEST), status=status.HTTP_400_BAD_REQUEST)

            Comments.objects.create_comment(serializer.validated_data, user=request.user)
            return Response(success_response(None, "Comment created successfully"), status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating comment: {e}")
            return Response(error_response(message="Something went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentRetrieveUpdateDeleteView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        try:
            comment = Comments.objects.get_comment_by_id(pk)
            if not comment:
                logger.warning(f"Comment fetch failed - not found: id={pk}")
                return Response(error_response(message="Comment not found", code=status.HTTP_404_NOT_FOUND), status=status.HTTP_404_NOT_FOUND)

            data = format_comment(comment)
            return Response(success_response(data, "Comment fetched successfully", include_data=True), status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching comment: id={pk}, error={e}")
            return Response(error_response(message="Something went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            comment = Comments.objects.get_comment_by_id(pk)
            if not comment:
                logger.warning(f"Comment update failed - not found: id={pk}")
                return Response(error_response(message="Comment not found", code=status.HTTP_404_NOT_FOUND), status=status.HTTP_404_NOT_FOUND)

            if comment.user != request.user:
                logger.warning(f"Comment update forbidden: user={request.user.id} tried to edit comment id={pk}")
                return Response(error_response(message="You are not allowed to edit this comment", code=status.HTTP_403_FORBIDDEN), status=status.HTTP_403_FORBIDDEN)

            serializer = CommentSerializer(data=request.data)
            if not serializer.is_valid():
                logger.warning(f"Comment update validation failed: id={pk}, errors={serializer.errors}")
                return Response(error_response("Validation error", status.HTTP_400_BAD_REQUEST), status=status.HTTP_400_BAD_REQUEST)

            Comments.objects.update_comment(pk, serializer.validated_data)
            return Response(success_response(None, "Comment updated successfully"), status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating comment: id={pk}, error={e}")
            return Response(error_response(message="Something went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            comment = Comments.objects.get_comment_by_id(pk)
            if not comment:
                logger.warning(f"Comment delete failed - not found: id={pk}")
                return Response(error_response(message="Comment not found", code=status.HTTP_404_NOT_FOUND), status=status.HTTP_404_NOT_FOUND)

            if comment.user != request.user:
                logger.warning(f"Comment delete forbidden: user={request.user.id} tried to delete comment id={pk}")
                return Response(error_response(message="You are not allowed to delete this comment", code=status.HTTP_403_FORBIDDEN), status=status.HTTP_403_FORBIDDEN)

            Comments.objects.delete_comment(pk)
            return Response(success_response(message="Comment deleted successfully", code=status.HTTP_204_NO_CONTENT), status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"Error deleting comment: id={pk}, error={e}")
            return Response(error_response(message="Something went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)