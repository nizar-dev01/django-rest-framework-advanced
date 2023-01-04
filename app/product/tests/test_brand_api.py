"""
Tests for brand APIs.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from product.serializers import BrandSerializer
from product.models import Brand

brand_payload = {
    "name": "Test Brand 1",
    "code": "test-brand-1"
}
LIST_BRAND_URL = reverse("product:brand-list")

class BrandAPITestsAuthenticated(TestCase):
    """Tests for brand APIs that require authentication."""

    def create_brand(self, payload = None):
        if not payload:
            payload = {
                "name": "Test Brand 1",
                "code": "test-brand-1"
            }

        return self.client.post(LIST_BRAND_URL, payload)

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "user@example.com",
            "userpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_brand_success(self):
        """Test create brand API is successful."""
        res = self.create_brand()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], brand_payload["name"])

    def test_list_brand_success(self):
        """Test list brand API is successful."""
        self.create_brand()
        self.create_brand()

        res_list = self.client.get(LIST_BRAND_URL)

        brands = Brand.objects.all()
        serilized_data = BrandSerializer(brands, many=True)

        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(serilized_data.data, res_list.data)


    def test_get_brand_success(self):
        """Test get brand API is successful."""
        brand = self.create_brand()

        bid = brand.data["id"]
        BRAND_DETAIL_URL = reverse("product:brand-detail", args=[bid])

        res = self.client.get(BRAND_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], bid)

    def test_update_brand_success(self):
        """Test update brand API is successful."""
        brand = Brand.objects.create(**{
            "name": "Temp Brand",
            "code": "temp-brand"
        })
        serialized = BrandSerializer(brand)

        new_data = {
            "name": "Temp Brand Changed",
            "id": serialized.data["id"]
        }
        bid = serialized.data["id"]
        BRAND_DETAIL_URL = reverse("product:brand-detail", args=[bid])

        res = self.client.patch(BRAND_DETAIL_URL, new_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], new_data["name"])

    def test_delete_brand_success(self):
        """Test delete brand API is successful."""
        brand = self.create_brand()

        bid = brand.data["id"]
        BRAND_DETAIL_URL = reverse("product:brand-detail", args=[bid])

        res = self.client.delete(BRAND_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)






