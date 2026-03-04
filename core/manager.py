from django.contrib.auth import get_user_model
# from .models import Posts
from .utils.choices import POST_STATUS_CHOICES, POST_DRAFT

class PostManager:
    def create_post(self, validated_data):
        """
        Create a new post with the given validated data and user.
        If no user is provided or user is anonymous, assign the first superuser.
        """
        # if not user or user.is_anonymous:
        #     user = User.objects.filter(is_superuser=True).first()
        return self.create(
            # created_by=user,
            title=validated_data['title'],
            description=validated_data['description'],
            status=validated_data.get('status', POST_DRAFT)
        )

    @staticmethod
    def update_post(instance, validated_data):
        """
        Update an existing post with validated data.
        Only updates fields provided in validated_data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance