"""
Test the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
GENERATE_TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")

def create_user(**params):
    user_model = get_user_model()
    user = user_model.objects.create_user(**params)
    return user

class PublicUserAPITests(TestCase):
    """Test the public features of the user API."""

    def setUp(self) -> None:
        self.client = APIClient()
        return super().setUp()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Test the password created is the same as the one passed in the payload
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

        # Test the password is not passed back in the API response
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name"
        }
        create_user(**payload) ## The aesterics will destructure the dictionary

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            "email": "test@example.com",
            "password": "pass",
            "name": "Test Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "testpass123"
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"]
        }
        res = self.client.post(GENERATE_TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "goodpass"
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": "badpass"
        }
        res = self.client.post(GENERATE_TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "goodpass"
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": ""
        }
        res = self.client.post(GENERATE_TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        user_details = {
            "name": "Unit Tester",
            "email": "test@example.com",
            "password": "testpass123"
        }
        self.user = create_user(**user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": "Unit Tester",
            "email": "test@example.com",
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {
            "name": "Updated Name",
            "password": "newpass123"
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
