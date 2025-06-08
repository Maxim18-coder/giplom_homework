from rest_framework import serializers
from .models import Post, Comment, Like, PostImage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'creation_date']
        read_only_fields = ['author', 'creation_date']

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image', 'creation_date']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'creation_date']
        read_only_fields = ['user', 'creation_date']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'creation_date',
            'comments', 'likes_count', 'images',
        ]
        read_only_fields = ['author', 'creation_date']

    def get_likes_count(self, obj):
        return obj.likes.count()