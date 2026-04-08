from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Posts
from ..serializers import PostSerializer
from core.utils.pagination import CustomLimitOffsetPagination
from core.utils.response import success_response, error_response
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging
logger = logging.getLogger(__name__)
from django.db.models import Prefetch


class PostListCreateView(APIView):

    pagination_class = CustomLimitOffsetPagination()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        keyword = request.query_params.get('search', None)
        if keyword:
            posts = Posts.objects.search_posts(keyword)
        else:
            posts = Posts.objects.get_all_posts()

        page = self.pagination_class.paginate_queryset(posts, request, view=self)
        return self.pagination_class.get_paginated_response(page)

    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data)

            if not serializer.is_valid():
                logger.warning(f"Post creation validation failed: {serializer.errors}")
                return Response(error_response("Information is invalid", status.HTTP_400_BAD_REQUEST), status=status.HTTP_400_BAD_REQUEST)

            Posts.objects.create_post(serializer.validated_data, user=request.user)

            return Response(success_response(None, "Post created successfully"), status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return Response(error_response(message="Something went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostRetrieveUpdateDeleteView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        post = Posts.objects.get_post_by_id(pk)

        if not post:
            logger.warning(f"Post not found: id={pk}")
            return Response(error_response(message="Post not found", code=status.HTTP_404_NOT_FOUND), status=status.HTTP_404_NOT_FOUND)

        data = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'status': post.status,
            'comments': list(post.comments.filter(is_deleted=False).values('id', 'body', 'created_at'))
        }

        return Response(success_response(data, "Post fetched successfully", include_data=True),status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            post = Posts.objects.get_post_by_id(pk)

            if not post:
                logger.warning(f"Post update failed - not found: id={pk}")
                return Response(error_response(message="Post not found", code=status.HTTP_404_NOT_FOUND), status=status.HTTP_404_NOT_FOUND)

            if post.user != request.user:
                logger.warning(f"Post update forbidden: user={request.user.id} tried to edit post id={pk}")
                return Response(error_response(message="You are not allowed to edit this post", code=status.HTTP_403_FORBIDDEN),status=status.HTTP_403_FORBIDDEN)

            serializer = PostSerializer(data=request.data)

            if not serializer.is_valid():
                logger.warning(f"Post update validation failed: id={pk}, errors={serializer.errors}")
                return Response(error_response("Validation error", status.HTTP_400_BAD_REQUEST),status=status.HTTP_400_BAD_REQUEST)

            updated_post = Posts.objects.update_post(pk, serializer.validated_data)
            return Response(success_response(None, "Post updated successfully"),status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating post: id={pk}, error={e}")
            return Response(error_response(message="Something went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            post = Posts.objects.get_post_by_id(pk)
            if not post:
                logger.warning(f"Post delete failed - not found: id={pk}")
                return Response(error_response(message="Post not found", code=status.HTTP_404_NOT_FOUND), status=status.HTTP_404_NOT_FOUND)

            if post.user != request.user:
                logger.warning(f"Post delete forbidden: user={request.user.id} tried to delete post id={pk}")
                return Response(error_response(message="You are not allowed to delete this post", code=status.HTTP_403_FORBIDDEN),status=status.HTTP_403_FORBIDDEN)

            Posts.objects.delete_post(pk)
            return Response(success_response(message="Post deleted successfully", code=status.HTTP_204_NO_CONTENT),status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"Error deleting post: id={pk}, error={e}")
            return Response(error_response(message="Something went wrong", code=status.HTTP_500_INTERNAL_SERVER_ERROR),status=status.HTTP_500_INTERNAL_SERVER_ERROR)