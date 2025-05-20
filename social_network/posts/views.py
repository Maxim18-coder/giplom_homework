from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Like
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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