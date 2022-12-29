from rest_framework import generics
from product.serializers import ProductSerializer
from .models import Product

class CreateProduct(generics.CreateAPIView):
    serializer_class = ProductSerializer

class UpdateProduct(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "brand"

    def perform_update(self, serializer):
        return super().perform_update(serializer)

class GetProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "brand"

class DeleteProduct(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "brand"

    # def perform_destroy(self, instance):
    #     return super().perform_destroy(instance)


class ListProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
