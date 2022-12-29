from django.test import TestCase
from blog.models import Blog
from django.core.exceptions import ValidationError

# Create your tests here.
def createBlog(data):
    blog = Blog(**data)
    blog.full_clean()
    blog.save()
    return blog

class BlogOperationsTests(TestCase):
    """Test the operations of the blog app"""
    def test_create_blog_success(self):
        blog_data = {
            "title": "Test blog",
            "content": "Content of the test blog",
            "slug": "test-blog-1"
        }
        blog = Blog(**blog_data)
        blog.save()

        saved_blog = Blog.objects.get(slug=blog_data["slug"])
        self.assertEqual(saved_blog.slug, blog_data["slug"])

    def test_create_blog_fail_with_invalid_content(self):
        blog_data = {
            "content": "Content",
            "slug": "test-blog-2",
        }

        with self.assertRaises(ValidationError):
            createBlog(blog_data)

    def test_delete_blog_success(self):
        blog_data = {
            "title": "Test blog",
            "content": "Content of the test blog",
            "slug": "test-blog-1"
        }
        blog = createBlog(blog_data)
        id = blog.id
        blog.delete()
        self.assertFalse(Blog.objects.filter(id=id).exists())

    def test_update_blog_success(self):
        blog_data = {
            "title": "Test blog",
            "content": "Content of the test blog",
            "slug": "test-blog-1"
        }
        blog = createBlog(blog_data)
        newSlug = "test-blog-changed-1"
        blog.save()
        blog.slug = newSlug
        blog.save()
        self.assertEqual(Blog.objects.get(id=blog.id).slug, newSlug)