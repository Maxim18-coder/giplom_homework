from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'content', 'creation_date']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many = True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'creation_date', 'content', 'comments', 'likes_count']

        def get_likes_count (self, obj):
            return obj.likes.count()
