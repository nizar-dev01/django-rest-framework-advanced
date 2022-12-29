from rest_framework import generics
from blog import serializers
from .models import Blog
class CreateBlogView(generics.CreateAPIView):
    serializer_class = serializers.BlogSerializer

class UpdateBlogView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = serializers.BlogSerializer
    lookup_field = "slug"

    def perform_update(self, serializer):
        print("::::::::::::::::::: - performing update operation - :::::::::::::::::::")
        serializer.save()
        return super().perform_update(serializer)


class ListBlogView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = serializers.BlogSerializer

class GetBlogView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = serializers.BlogSerializer
    lookup_field = "slug"