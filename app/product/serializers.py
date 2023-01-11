from rest_framework.serializers import ModelSerializer
from .models import Product
from .models import Brand

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "brand"
        ]

class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"