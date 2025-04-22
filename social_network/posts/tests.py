from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password = 'test_password')
        self.post = Post.objects.create_user(title='test_title', content='test_content', author=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'test_title')
        self.assertEqual(self.post.content, 'test_content')
        self.assertEqual(self.post.author.username, 'test_user')

class CommentModelTest(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username = 'test_user_1', password='test_password_1')
        self.user_2 = User.objects.create_user(username = 'test_user_2', password='test_password_2')
        self.post = Post.objects.create_uder(title='test_title_2', content='test_content_2', author=self.user_1)
        self.comment = Comment.objects.create(author=self.user_2, post=self.post, content='test_comment')

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'test_comment')
        self.assertEqual(self.comment.author.username, 'test_user_2')



