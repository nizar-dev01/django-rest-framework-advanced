"""
Test the Blog API.
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from blog.models import Blog

def create_blog():
    blog_data = {
        "title": "Test Blog Post",
        "content": "The content of the blog created during unit testing, which contains more than 20 characters to bypass the content validation.",
        "slug": "test-blog-1"
    }
    return Blog.objects.create(**blog_data)

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
        blog = create_blog()

        update_blog_data = {
            "title": "Test blog - Edited by the test",
            "content": "Content of the test blog",
            "slug": "test-blog-1"
        }

        BLOG_UPDATE_URL = reverse("blog:update", args=[blog.slug])

        updated_blog = self.client.put(BLOG_UPDATE_URL, update_blog_data)
        self.assertEqual(updated_blog.status_code, status.HTTP_200_OK)
        self.assertNotEqual(blog.title, updated_blog.json()["title"])

    def test_get_blog_success(self):
        """Test retrieving a single blog post is successful."""
        create_blog()

        slug = "test-blog-1"
        GET_BLOG_URL = reverse("blog:get", args=[slug])
        blog = self.client.get(GET_BLOG_URL)
        self.assertEqual(blog.json()["slug"], slug)

    def test_list_blogs_success(self):
        """Test listing all the blogs is successful."""
        LIST_BLOG_URL = reverse("blog:list")
        res = self.client.get(LIST_BLOG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)