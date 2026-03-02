from django.urls import path
from . import posts_views

urlpatterns = [
    path('posts/', posts_views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', posts_views.PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
]