from django.test import TestCase

from core.extensions.test import sample_board, sample_user, sample_topic
from boards.models import Post


class BoardTests(TestCase):
    """Tests for the board model"""

    def setUp(self):
        self.board = sample_board()

    def test_board_str(self):
        """Test the string representation"""
        self.assertEqual(str(self.board), self.board.title)


class TopicTests(TestCase):
    """Tests for the topic model"""

    def setUp(self):
        self.user = sample_user()
        self.board = sample_board()
        self.topic = sample_topic(self.user.profile, self.board)

    def test_topic_str(self):
        """Test the string representation"""
        self.assertEqual(str(self.topic), self.topic.title)


class PostTests(TestCase):
    """Tests for the post model"""

    def setUp(self):
        self.user = sample_user()
        self.board = sample_board()
        self.topic = sample_topic(self.user.profile, self.board)
        self.post = Post.objects.create(author=self.user.profile, topic=self.topic, message='Test post')

    def test_post_str(self):
        """Test the string representation"""
        self.assertEqual(str(self.post), self.post.message[:20])

    def test_edit_post(self):
        """Test editing a post's message"""
        self.assertIsNone(self.post.edited_at)
        new_message = 'New post message'
        self.post.edit_message(new_message)
        self.assertEqual(self.post.message, new_message)
        self.assertIsNotNone(self.post.edited_at)
