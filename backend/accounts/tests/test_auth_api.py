from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from core.utils.testutils import sample_user


CREATE_USER_URL = reverse('accounts:create')
TOKEN_URL = reverse('accounts:token')
MANAGE_URL = reverse('accounts:manage')


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {'email': 'test@marsimon.com', 'password': 'testing123'}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_exists(self):
        """Test creating user that already exists"""
        payload = {'email': 'test@marsimon.com', 'password': 'testing123'}
        User.objects.create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'test@marsimon.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@marsimon.com', 'password': 'password123'}
        User.objects.create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that a token is not created if invalid credentials are given"""
        User.objects.create_user(email='test@marsimon.com', password='password123')
        payload = {'email': 'test@marsimon.com', 'password': 'wrongpassword'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created when user does not exist"""
        payload = {'email': 'test@marsimon.com', 'password': 'password123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_update_user_password_patch(self):
        """Test updating the user's password"""
        payload = {'password': 'newpassword123'}
        res = self.client.patch(MANAGE_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))

    def test_update_user_password_put(self):
        """Test updating the user's password"""
        payload = {'email': 'testing@marsimon.com', 'password': 'newpassword123'}
        res = self.client.put(MANAGE_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))
