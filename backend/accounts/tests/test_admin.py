from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from core.utils.testutils import sample_user


class AdminSiteTests(TestCase):

    def setUp(self):
        self.admin_user = sample_user(superuser=True)
        self.client.force_login(self.admin_user)
        self.user = sample_user(email='test@marsimon.com')

    def test_users_listed(self):
        """Users are listed on user page"""
        url = reverse('admin:accounts_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)

    def test_users_change_page(self):
        url = reverse('admin:accounts_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_users_add_page(self):
        url = reverse('admin:accounts_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
