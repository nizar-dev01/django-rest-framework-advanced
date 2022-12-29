from rest_framework import serializers
from blog.models import Blog

class BlogSerializer(serializers.Serializer):
    class Meta:
        model = Blog
        fields = "__all__"

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)