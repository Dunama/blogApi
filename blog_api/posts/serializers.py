from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'body',
            'cover_photo',
            'author',
            'likes_count',
            'liked_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['author', 'likes_count', 'liked_by', 'created_at', 'updated_at']

    def get_likes_count(self, obj: Post) -> int:
        return obj.likes.count()

    def get_liked_by(self, obj: Post):
        return list(obj.likes.values_list('username', flat=True))
