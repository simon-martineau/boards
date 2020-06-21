from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import Profile
from core.utils.testutils import sample_user


PROFILE_BASE_URL = '/api/users/profiles'


def get_profile_url(profile: Profile):
    """Utility method to retrieve a profile's url"""
    return reverse('accounts:profile', args=[profile.id])


class PublicProfileApiTests(TestCase):
    """Tests for the publicly available profile api"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.user.profile.username = 'TestUsername'

    def test_retrieve_public_profile(self):
        """Test retrieving a profile that is not self owned"""
        res = self.client.get(get_profile_url(self.user.profile))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['is_self'], False)

    def test_create_or_delete_profile_fails(self):
        """Test that creating or deleting a profile fails"""
        payload = {'user': self.user.id, 'username': 'someusername'}
        res_post = self.client.post(PROFILE_BASE_URL, payload)
        res_delete = self.client.delete(get_profile_url(self.user.profile))

        self.assertIn(res_post.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND])
        self.assertEqual(res_delete.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modifying_public_profile_fails(self):
        """Test that updating another one's profile fails"""
        # Put
        payload = {'user': self.user.id, 'username': 'someusername'}
        res_put = self.client.put(get_profile_url(self.user.profile), payload)
        payload.pop('user')
        res_patch = self.client.patch(get_profile_url(self.user.profile), payload)

        self.assertEqual(res_put.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_patch.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProfileApiTests(TestCase):
    """Tests for the private profile api"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.user.profile.username = 'TestUsername'
        self.client.force_authenticate(self.user)

    def test_retrieve_another_profile(self):
        """Test retrieving a profile that is not self owned (mostly checking is_self)"""
        res = self.client.get(get_profile_url(self.user.profile))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['is_self'], True)

    def test_patch_profile(self):
        """Test updating own's profile with patch"""
        payload = {'username': 'AnotherUsername'}
        res = self.client.patch(get_profile_url(self.user.profile), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.username, payload['username'])

    def test_put_profile(self):
        """Test updating own's profile with put"""
        payload = {'username': 'SomeUsername'}
        res = self.client.put(get_profile_url(self.user.profile), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.username, payload['username'])
