"""
Test the Blog API.
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class BlogAPITest(TestCase):
    """Test the endpoints of the blog API."""
    def setUp(self):
        self.client = APIClient()
        return super().setUp()

    def test_blog_create_api_success(self):
        """Test creating a blog is scuccessful."""
        blog_data = {
            "title": "Test Blog Post",
            "content": "The content of the blog created during unit testing, which contains more than 20 characters to bypass the content validation.",
            "slug": "test-blog-post"
        }
        BLOG_CREATE_URL = reverse("blog:create")
        res = self.client.post(BLOG_CREATE_URL, blog_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_blog_update_api_success(self):
        """Test updating a blog post is working"""
        pass
