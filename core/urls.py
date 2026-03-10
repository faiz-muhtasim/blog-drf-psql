from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentRetrieveUpdateDeleteView.as_view(), name='comment-detail'),
    path('otp/', views.OTPListCreateView.as_view(), name='otp-list-create'),
    path('otp/verify/', views.OTPVerifyView.as_view(), name='otp-verify'),
    path('otp/<int:pk>/', views.OTPRetrieveDeleteView.as_view(), name='otp-detail'),
]