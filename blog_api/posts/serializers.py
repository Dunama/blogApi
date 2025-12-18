from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    cover_photo_url = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'body',
            'cover_photo',
            'cover_photo_url',
            'author',
            'likes_count',
            'liked_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['author', 'likes_count', 'liked_by', 'created_at', 'updated_at']

    def get_cover_photo_url(self, obj: Post) -> str | None:
        if not obj.cover_photo:
            return None
        request = self.context.get('request')
        url = obj.cover_photo.url
        return request.build_absolute_uri(url) if request else url

    def get_likes_count(self, obj: Post) -> int:
        return obj.likes.count()

    def get_liked_by(self, obj: Post):
        return list(obj.likes.values_list('username', flat=True))
