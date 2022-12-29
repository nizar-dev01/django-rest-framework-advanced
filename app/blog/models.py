from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def validate_blog_content(value):
    if len(value) < 20:
        raise ValidationError("The content of the blog must be at least 20 characters")

class Blog(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(validators=[validate_blog_content], blank=False, null=False)
    slug = models.CharField(max_length=250, blank=False, null=False, unique=True)
