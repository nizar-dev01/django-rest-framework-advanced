from django.test import TestCase
from product.models import Brand

payload = {
    "name": "test-brand-1",
    "code": "test-brand-1"
}

def createBrand(data=payload):
    return Brand.objects.create(**data)

class BrandModelCrudTests(TestCase):
    """Tests for brand crud operations on Brand model."""

    def test_brand_create_success(self):
        brand = createBrand()

        self.assertEqual(brand.name, payload["name"])
        self.assertEqual(brand.code, payload["code"])
