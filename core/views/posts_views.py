from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Posts
from ..serializers import PostSerializer
from core.utils.pagination import CustomLimitOffsetPagination
from core.utils.response import success_response, error_response


class PostListCreateView(APIView):

    pagination_class = CustomLimitOffsetPagination()

    def get(self, request):
        keyword = request.query_params.get('search', None)

        if keyword:
            posts = Posts.objects.search_posts(keyword)
        else:
            posts = Posts.objects.get_all_posts()
        paginator = self.pagination_class
        page = paginator.paginate_queryset(posts, request, view=self)

        data = []
        for post in page:
            data.append({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'status': post.status,
                'comments': list(post.comments.filter(is_deleted=False).values('id', 'body', 'created_at'))
            })

        return paginator.get_paginated_response(data)

    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(error_response(serializer.errors, "Validation error", 400), status=status.HTTP_400_BAD_REQUEST)
            post = Posts.objects.create_post(serializer.validated_data)
            return Response(success_response(PostSerializer(post).data, "Post created successfully", 201), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(error_response(message=str(e), code=500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostRetrieveUpdateDeleteView(APIView):

    def get(self, request, pk):
        post = Posts.objects.get_post_by_id(pk)
        if not post:
            return Response(error_response(message="Post not found", code=404), status=status.HTTP_404_NOT_FOUND)
        data = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'status': post.status,
            'comments': list(post.comments.filter(is_deleted=False).values('id', 'body', 'created_at'))
        }
        return Response(success_response(data, "Post fetched successfully", include_data=True), status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            serializer = PostSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(error_response(serializer.errors, "Validation error", 400),
                                status=status.HTTP_400_BAD_REQUEST)
            updated_post = Posts.objects.update_post(pk, serializer.validated_data)
            if not updated_post:
                return Response(error_response(message="Post not found", code=404), status=status.HTTP_404_NOT_FOUND)
            return Response(success_response(PostSerializer(updated_post).data, "Post updated successfully"),
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(error_response(message=str(e), code=500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            deleted = Posts.objects.delete_post(pk)
            if not deleted:
                return Response(error_response(message="Post not found", code=404), status=status.HTTP_404_NOT_FOUND)
            return Response(success_response(message="Post deleted successfully", code=204),
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(error_response(message=str(e), code=500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)