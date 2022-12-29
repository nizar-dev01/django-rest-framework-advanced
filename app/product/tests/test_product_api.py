from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Product
import random

payload = {
    "name": "Test Product",
    "brand": "test-brand",
}

def CreateProduct(data):
    return Product.objects.create(**data)

class TestProductAPI(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Create
    def test_create_product_api(self):
        """Test create product API"""
        CREATE_PRODUCT_URL = reverse("product:create")
        self.assertIsNotNone(CREATE_PRODUCT_URL)

        res = self.client.post(CREATE_PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # Update
    def test_update_product_api(self):
        """Test update product API."""
        product = CreateProduct(payload)
        UPDATE_PRODUCT_URL = reverse("product:update", args=[product.brand])

        update_payload = {
            "name": "Test Product Edited",
            "brand": "test-brand-edited"
        }

        self.client.put(UPDATE_PRODUCT_URL, update_payload)
        updated_product = Product.objects.get(brand=update_payload["brand"])

        self.assertNotEqual(product.name, updated_product.name)
        self.assertNotEqual(product.brand, updated_product.brand)

    # List
    def test_list_products_api(self):
        """Test list producst API."""
        payloads = [payload, {
            "name": "Test Product 1",
            "brand": "test-brand-1",
        }]
        for p in payloads:
            CreateProduct(p)

        LIST_PRODUCTS_URL = reverse("product:list")
        res = self.client.get(LIST_PRODUCTS_URL)
        product_count = len(res.json())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(product_count, len(payloads))




    # Detail
    def test_product_detail_api(self):
        """Test product detail API."""
        payloads = [
            payload,
            {
                "name": "Test Product 1",
                "brand": "test-brand-1",
            },
            {
                "name": "Test Product 2",
                "brand": "test-brand-2",
            },
            {
                "name": "Test Product 3",
                "brand": "test-brand-3",
            },
            {
                "name": "Test Product 4",
                "brand": "test-brand-5",
            }
        ]
        for p in payloads:
            CreateProduct(p)

        random_index = round(random.random() * (len(payloads) - 1))
        random_product_brand = payloads[random_index]["brand"]
        PRODUCT_DETAIL_URL = reverse("product:detail", args=[random_product_brand])
        res = self.client.get(PRODUCT_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()["brand"], random_product_brand)

    # Delete
    def test_product_destroy_api(self):
        """Test product destroy API."""
        payloads = [
            payload,
            {
                "name": "Test Product 1",
                "brand": "test-brand-1",
            },
            {
                "name": "Test Product 2",
                "brand": "test-brand-2",
            }
        ]
        for p in payloads:
            CreateProduct(p)

        random_index = round(random.random() * (len(payloads) - 1))
        random_product_brand = payloads[random_index]["brand"]

        PRODUCT_DESTROY_URL = reverse("product:destroy", args=[random_product_brand])
        res = self.client.delete(PRODUCT_DESTROY_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
