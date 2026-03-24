from .posts_views import PostListCreateView, PostRetrieveUpdateDeleteView
from .comment_views import CommentListCreateView, CommentRetrieveUpdateDeleteView
from .otp_views import OTPListCreateView, OTPVerifyView, OTPRetrieveDeleteView

# views/__init__.py
from .auth_views    import RegisterView, ProfileView
from .posts_views   import *      # or list specific classes
from .comment_views import *
from .otp_views     import *