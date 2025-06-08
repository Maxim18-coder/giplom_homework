from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Like, Comment, PostImage
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, PostImageSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise permissions.PermissionDenied("Вы не можете редактировать этот пост.")
        serializer.save()

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like_obj, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            return Response({'detail': 'Вы уже поставили лайк.'}, status=400)

        return Response({'likes_count': post.likes.count()})

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        deleted_count, _ = Like.objects.filter(post=post, user=user).delete()

        return Response({'likes_count': post.likes.count()})