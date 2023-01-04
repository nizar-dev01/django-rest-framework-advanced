from rest_framework import (
    generics,
    viewsets,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from product.serializers import (
    ProductSerializer,
    BrandSerializer
)
from .models import (
    Product,
    Brand
)


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

class BrandViewSet(viewsets.ModelViewSet):
    """Viewset for Brand."""
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ TokenAuthentication ]
