from dataclasses import fields

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User


User = get_user_model()


class Post(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', related_name = 'post', on_delete = models.CASCADE)
    creation_date = models.DateTimeField(default = timezone.now)
    tags = models.ManyToManyField('Tag', blank=True)
    likes = models.ManyToManyField('auth.User', through = 'Like', related_name = 'Liked_posts', blank=True)

    class Meta:
        db_table = 'blog_posts'
        ordering = ['-creation_date']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['creation_date'], name='creation_date_idx')
        ]

def publish(self):
    self.published_date = timezone.now()
    self.save()

def like(self, user):
    Like.objects.create (post = self, user = user)

def unlike(self , user):
    Like.objects.filter (post = self, user = user).delete()

def __str__ (self):
    return  self.title

class PostImage(models.Model):
     post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'images')
     image = models.ImageField(upload_to = 'post_images/')
     creation_date = models.DateTimeField(auto_now_add = True)

     def __str__ (self):
        return f"image for {self.post.title}"

class Like(models.Model):
    objects = None
    user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"


class Comment(models.Model):
    objects = None
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'comments')
    content = models.TextField(max_length=500)
    creation_date = models.DateTimeField(default = timezone.now)
    
    class Meta:
        ordering = ['-creation_date']

        def __str__ (self):
          return f"Comment by {self.author.username} on {self.post.title}"
