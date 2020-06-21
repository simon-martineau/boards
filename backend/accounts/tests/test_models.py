from django.test import TestCase

from core.utils.testutils import sample_user

from accounts.models import User, Profile


class UserModelTests(TestCase):

    def test_create_user_with_email_success(self):
        """Tests if user creation with email is successful"""
        email = 'test@marsimon.com'
        password = 'testpassword123'

        user = User.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests if the email for a new user is normalized"""
        email = 'Test@MARSIMON.COM'
        user = User.objects.create_user(email, 'test123')
        self.assertEqual(user.email, 'Test@marsimon.com')

    def test_new_user_invalid_email(self):
        """Tests if creating user with no email raises an error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Tests creating a new superuser"""
        user = User.objects.create_superuser(
            'test@marsimon.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class ProfileModelTests(TestCase):

    def setUp(self):
        self.user = sample_user()

    def test_profile_str(self):
        """Test the profile string respresentation"""
        self.user.profile.username = "testing username"
        self.assertEqual(str(self.user.profile), f'{self.user.profile.username} ({self.user.email})')

    def test_profile_gets_created_on_user_create(self):
        """Test that an associated profile gets create with a user"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertTrue(hasattr(self.user.profile, 'username'))

    def test_default_username_gets_created(self):
        """Test that a default unique username gets created with the model"""
        self.assertNotEqual(len(self.user.profile.username), 0)

    def test_set_username_successful(self):
        """Test setting a new username successfully"""
        result = self.user.profile.set_username('newusername')
        self.assertTrue(result)
        self.assertEqual(self.user.profile.username, 'newusername')

    def test_set_username_already_taken(self):
        """Test setting a new username with name already taken"""
        other_user = sample_user(email='another@marsimon.com')
        other_user.profile.username = 'newprofileusername'
        other_user.profile.save()

        current_username = self.user.profile.username
        result = self.user.profile.set_username(other_user.profile.username)

        self.assertFalse(result)
        self.assertNotEqual(self.user.profile.username, other_user.profile.username)
        self.assertEqual(self.user.profile.username, current_username)
        self.assertFalse(self.user.profile.is_username_chosen)
