from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Posts
from ..serializers import PostSerializer
from core.utils.pagination import CustomLimitOffsetPagination
# from .manager import PostManager

class PostListCreateView(APIView):
    pagination_class = CustomLimitOffsetPagination()

    def get(self, request):
        posts = Posts.objects.get_all_posts()
        print(len(posts))
        paginator = self.pagination_class
        page = paginator.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            post = Posts.objects.create_post(serializer.validated_data)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostRetrieveUpdateDeleteView(APIView):

    def get(self, request, pk):
        post = Posts.objects.get_post_by_id(pk)
        if not post:
            return Response(
                {
                    "success": False,
                    "code": 404,
                    "message": "Post not found",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "success": True,
                "code": 200,
                "message": "Post fetched successfully",
                "data": PostSerializer(post).data,
            },
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        try:
            post = Posts.objects.get_post_by_id(pk)
            if not post:
                return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            updated_post = Posts.objects.update_post(post, serializer.validated_data)
            return Response(PostSerializer(updated_post).data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            post = Posts.objects.get_post_by_id(pk)
            if not post:
                return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
            Posts.objects.delete_post(post)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)