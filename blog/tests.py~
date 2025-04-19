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
