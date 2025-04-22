from django.test import TestCase

# Create your tests here.
# blog/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post
import json

class CreatePostAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create-post')
        self.valid_payload = {
            "title": "Test Post",
            "content": "This is a test post content."
        }
        self.invalid_payload = {
            "title": "",  # Title is empty
            "content": ""
        }

    def test_create_post_success(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, "Test Post")

    def test_create_post_failure(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        # This should fail — but your current code might return 201 anyway
        # Reviewers can suggest adding validation
        self.assertNotEqual(Post.objects.count(), 1)

class DeletePostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = Post.objects.create(title='Test Post', content='This post is for testing delete.')

    def test_delete_existing_post(self):
        response = self.client.delete(f'/api/posts/delete/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('deleted_post', response.json())

    def test_delete_nonexistent_post(self):
        response = self.client.delete('/api/posts/delete/9999/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_delete_with_invalid_method(self):
        response = self.client.get(f'/api/posts/delete/{self.post.id}/')
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())

class GetAllPostsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get-all-posts')
        # Create sample posts
        Post.objects.create(title='Post 1', content='Content 1')
        Post.objects.create(title='Post 2', content='Content 2')

    def test_get_all_posts_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('posts', data)
        self.assertEqual(len(data['posts']), 2)

        # Check the structure of the first post
        first_post = data['posts'][0]
        self.assertIn('id', first_post)
        self.assertIn('title', first_post)
        self.assertIn('content', first_post)
        self.assertIn('created_at', first_post)

    def test_get_all_posts_wrong_method(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        data = response.json()
        self.assertIn('error', data)