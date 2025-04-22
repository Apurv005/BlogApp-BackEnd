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
            "title": "",
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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Post.objects.count(), 0)


class DeletePostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = Post.objects.create(title='Test Post', content='This post is for testing delete.')
        self.url = reverse('delete-post', kwargs={'post_id': self.post.id})
        self.invalid_url = reverse('delete-post', kwargs={'post_id': 9999})

    def test_delete_existing_post(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('deleted_post', response.json())

    def test_delete_nonexistent_post(self):
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_delete_with_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())


class UpdatePostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = Post.objects.create(title='Original Title', content='Original Content')
        self.valid_payload = {
            "title": "Updated Title",
            "content": "Updated Content"
        }
        self.invalid_payload = {
            "title": "",
            "content": ""
        }
        self.update_url = reverse('update-post', kwargs={'pk': self.post.id})
        self.invalid_update_url = reverse('update-post', kwargs={'pk': 9999})

    def test_update_existing_post_success(self):
        response = self.client.put(
            self.update_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_update_nonexistent_post(self):
        response = self.client.put(
            self.invalid_update_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_update_with_invalid_data(self):
        response = self.client.put(
            self.update_url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_update_with_invalid_method(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())
