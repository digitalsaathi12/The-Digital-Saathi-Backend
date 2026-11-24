from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "img_path",
            "published_at",
            "is_published",
            "created_at",
            "modified_at",
        ]