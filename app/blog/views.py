from rest_framework import generics
from blog.serializers import BlogSerializer

class CreateBlogView(generics.CreateAPIView):
    serializer_class = BlogSerializer
