from django.contrib import admin
from .models import Like, Comment, Post, PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'creation_date')
    search_fields = ('title',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'creation_date', 'post')
    search_fields = ('content',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'timestamp',)

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    like_display = ('post', 'image', 'creation_date',)