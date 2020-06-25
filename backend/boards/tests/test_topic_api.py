from django.test import RequestFactory

from rest_framework.reverse import reverse
from rest_framework import status

from core.extensions.test import APITestCase, sample_topic, sample_user, sample_board
from boards.models import Board, Topic, Post
from boards.serializers import TopicSerializer, TopicListSerializer, CreateTopicSerializer


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

        url = get_topic_url(self.board)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        fields_desired = ('id', 'board', 'title', 'starter', 'post_count', 'first_post', 'created_at')
        serializer = TopicListSerializer(self.board.topics, many=True, context={'request': RequestFactory().get(url)})
        self.assertEqual(res.data, serializer.data)
        self.assertAllIn(fields_desired, res.data[0].keys())
        self.assertAllIn(('username', 'href'), res.data[0]['starter'])

    def test_retrieve_topic_detail(self):
        """Test retriving a topic's details"""
        url = get_topic_url(self.board, self.topic)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        fields_desired = ('id', 'board', 'title', 'starter', 'posts', 'created_at')
        serializer = TopicSerializer(self.topic, context={'request': RequestFactory().get(url)})
        self.assertEqual(res.data, serializer.data)
        self.assertAllIn(fields_desired, res.data.keys())
        self.assertAllIn(('username', 'href'), res.data['starter'])

    def test_create_topic_requires_auth(self):
        """Test that authentication is required to create a topic"""
        topic_count = Topic.objects.all().count()
        url = get_topic_url(self.board)
        payload = {
            'title': 'Some topic title',
            'message': 'Some message'
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Topic.objects.all().count(), topic_count)

    def test_update_topic_requires_auth(self):
        """Test that updating a topic requires authentification"""
        url = get_topic_url(self.board)
        payload = {
            'title': 'Some new topic title'
        }
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.topic.refresh_from_db()
        self.assertNotEqual(self.topic.title, payload['title'])


class PrivateTopicApiTests(APITestCase):
    """Tests for the private topic api"""

    def setUp(self):
        self.board = sample_board()
        self.user = sample_user()
        self.topic = sample_topic(starter=self.user.profile, board=self.board)
        self.post = Post.objects.create(author=self.user.profile, message='Test post message', topic=self.topic)
        self.client.force_authenticate(self.user)

    def test_create_topic_successful(self):
        """Test creating a topic"""
        url = get_topic_url(self.board)
        payload = {
            'title': 'A new topic',
            'message': 'Message about the topic'
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertAllIn(('id', 'board', 'title', 'starter', 'posts', 'created_at'), res.data)
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['posts'][0]['message'], payload['message'])
        self.assertIsNotNone(res.data['starter'])

    def test_update_topic_put_successful(self):
        """Test successfully updating a topic with a put request"""
        url = get_topic_url(self.board, self.topic)
        payload = {
            'title': 'New topic title'
        }
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, payload['title'])

    def test_update_topic_patch_successful(self):
        """Test successfully updating a topic with a put request"""
        url = get_topic_url(self.board, self.topic)
        payload = {
            'title': 'New topic title'
        }
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.title, payload['title'])

    def test_update_topic_requires_ownership(self):
        """Test that updating a topic requires the ownership"""
        new_user = sample_user(email='newuser@marsimon.com')
        new_topic = sample_topic(board=self.board, starter=new_user.profile, title='Topic from another user')

        url = get_topic_url(self.board, new_topic)
        payload = {
            'title': 'Modified topic title'
        }
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        new_topic.refresh_from_db()
        self.assertNotEqual(new_topic.title, payload['title'])
