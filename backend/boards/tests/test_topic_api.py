from rest_framework.reverse import reverse
from rest_framework import status

from core.extensions.test import APITestCase, sample_topic, sample_user, sample_board
from boards.models import Board, Topic, Post
from boards.serializers import TopicSerializer


def get_topic_url(board: Board, topic: Topic = None) -> str:
    """Get the url for topics or for a specific topic if topic is specified"""
    if topic is None:
        return reverse('boards:boards-topic-list', args=(board.id,))
    return reverse('boards:boards-topic-detail', args=(board.id, topic.id))


class PublicTopicApiTests(APITestCase):
    """Tests for the publicly available topic api"""

    def setUp(self):
        self.board = sample_board()
        self.user = sample_user()
        self.topic = sample_topic(starter=self.user.profile, board=self.board)
        self.post = Post.objects.create(author=self.user.profile, message='Test post message', topic=self.topic)

    def test_retrieve_topic_list(self):
        """Test retrieving a topic list from a board"""
        sample_topic(starter=self.user.profile, board=self.board, title='Other testing topic')

        res = self.client.get(get_topic_url(self.board))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        fields_desired = ('id', 'board', 'title', 'starter', 'post_count', 'created_at')
        serializer = TopicSerializer(self.board.topics, fields=fields_desired, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertAllIn(fields_desired, res.data[0].keys())

    def test_retrieve_topic_detail(self):
        """Test retriving a topic's details"""
