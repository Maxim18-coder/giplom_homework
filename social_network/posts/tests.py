from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Post

class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Title', content='Test Content', author=self.user)

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/posts/', {'title': 'New Post', 'content': 'Some content'})
        self.assertEqual(response.status_code, 201)

    def test_update_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/posts/{self.post.id}/', {'title': 'Updated Title'})
        self.assertEqual(response.status_code, 200)
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.title, 'Updated Title')

    def test_delete_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post.id)
