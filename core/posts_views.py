from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Posts
from .serializers import PostSerializer
# from .manager import PostManager

class PostListCreateView(APIView):
    """
    GET: List all posts
    POST: Create a new post
    """
    def get(self, request):
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request): 
        try:
            serializer = PostSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            post = Posts.objects.create_post(serializer.validated_data)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        except:
            Response("Something went wrong!!!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class PostRetrieveUpdateDeleteView(APIView):
    """
    GET: Retrieve a post
    PUT: Update a post
    DELETE: Delete a post
    """
    def get_object(self, pk):
        try:
            return Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            post = self.get_object(pk)
            if not post:
                return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(data=request.data)
            if not serializer.is_valid(): 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            updated_post = Posts.objects.update_post(post, serializer.validated_data)
            return Response(PostSerializer(updated_post).data)
        except:
            Response("Something went wrong!!!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self, request, pk):
        try:
            post = self.get_object(pk)
            if not post:
                return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            Response("Something went wrong!!!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)