from django.contrib.auth import get_user_model
from .models import Posts

class PostManager:

    @staticmethod
    def create_post(validated_data):
        """
        Create a new post with the given validated data and user.
        If no user is provided or user is anonymous, assign the first superuser.
        """
        # if not user or user.is_anonymous:
        #     user = User.objects.filter(is_superuser=True).first()
        return Posts.objects.create(
            # created_by=user,
            title=validated_data['title'],
            description=validated_data['description'],
            status=validated_data.get('status', Posts.DRAFT)
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