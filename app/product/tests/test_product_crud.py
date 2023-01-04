from django.test import TestCase
from product.models import Product

payload = {
    "name": "test-product-1",
    "brand": "test-brand-1"
}

def createProduct(data):
    return Product.objects.create(**data)

class ProductCrudTest(TestCase):
    """Test CRUD operations on product model is operational."""
    def test_create_product_success(self):
        product = createProduct(payload)
        self.assertEquals(product.name, payload["name"])

    def test_update_product_success(self):
        product = createProduct(payload)
        product.name = product.name+"-updated"
        product.save()
        updated = Product.objects.get(name=product.name)
        self.assertNotEqual(updated.name, payload["name"])
