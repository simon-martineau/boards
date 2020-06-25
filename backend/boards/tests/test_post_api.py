from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from core.extensions.test import sample_board, sample_topic, sample_user, APITestCase
from boards.models import Board, Topic, Post
from boards.serializers import PostSerializer


def get_post_url(board: Board, topic: Topic, post: Post = None) -> str:
    """Returns the post detail url if a post is given, else the post list url"""
    if post is None:
        return reverse('boards:boards-topics-post-list', args=(board.id, topic.id))
    return reverse('boards:boards-topics-post-detail', args=(board.id, topic.id, post.id))


class PublicPostApiTests(APITestCase):
    """Tests for the publicly available topic api"""

    def setUp(self):
        self.board = sample_board()
        self.user = sample_user()
        self.topic = sample_topic(starter=self.user.profile, board=self.board)
        self.post = Post.objects.create(author=self.user.profile, message='Test post message', topic=self.topic)

    def test_retrieve_post_list(self):
        """Test retrieving a list of posts for a given topic"""
        Post.objects.create(author=self.user.profile, message='Another post message', topic=self.topic)
        url = get_post_url(self.board, self.topic)
        res = self.client.get(url)

        fields_desired = ('id', 'topic', 'author', 'created_at', 'edited_at', 'message')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertAllIn(fields_desired, res.data[0])

        serializer = PostSerializer(Post.objects.filter(topic_id=self.topic.id), many=True,
                                    context={'request': APIRequestFactory().get(url)})
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_post_detail(self):
        """Test retrieving the details of a given post"""
        url = get_post_url(self.board, self.topic, self.post)
        res = self.client.get(url)

        fields_desired = ('id', 'topic', 'author', 'created_at', 'edited_at', 'message')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertAllIn(fields_desired, res.data)

        serializer = PostSerializer(Post.objects.get(topic_id=self.topic.id),
                                    context={'request': APIRequestFactory().get(url)})
        self.assertEqual(res.data, serializer.data)

    def test_create_post_requires_auth(self):
        """Test that creating a post requires authentication"""
        post_count = self.topic.posts.count()
        url = get_post_url(self.board, self.topic)
        payload = {
            'message': 'New post message!'
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.topic.posts.count(), post_count)

    def test_update_post_requires_auth(self):
        """Test that updating a post requires authentication"""
        url = get_post_url(self.board, self.topic, self.post)
        payload = {
            'message': 'Edited message'
        }
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.message, payload['message'])


class PrivatePostApiTests(APITestCase):
    """Tests for the private post api"""

    def setUp(self):
        self.board = sample_board()
        self.user = sample_user()
        self.topic = sample_topic(starter=self.user.profile, board=self.board)
        self.post = Post.objects.create(author=self.user.profile, message='Test post message', topic=self.topic)
        self.client.force_authenticate(self.user)

    def test_create_post_successful(self):
        """Test successfully creating a post with a post request"""
        url = get_post_url(self.board, self.topic)
        payload = {
            'message': 'New post message testing'
        }
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        fields_desired = ('id', 'topic', 'author', 'created_at', 'edited_at', 'message')
        self.assertAllIn(fields_desired, res.data)

        serializer = PostSerializer(Post.objects.get(id=res.data['id']),
                                    context={'request': APIRequestFactory().get(url)})
        data = res.data
        data['topic'] = int(data['topic'])  # Workaround for a bug that makes post requests return the topic id as a str

        self.assertEqual(data, serializer.data)
        self.assertIsNone(res.data['edited_at'])

    def test_update_post_patch_successful(self):
        """Test successfully updating post with a patch request"""
        starting_edited_at = self.post.edited_at
        url = get_post_url(self.board, self.topic, self.post)
        payload = {
            'message': 'Newly edited message'
        }
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.message, payload['message'])
        self.assertNotEqual(self.post.edited_at, starting_edited_at)

    def test_update_post_put_successful(self):
        """Test successfully updating post with a put request"""
        starting_edited_at = self.post.edited_at
        url = get_post_url(self.board, self.topic, self.post)
        payload = {
            'message': 'Newly edited message'
        }
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.message, payload['message'])
        self.assertNotEqual(self.post.edited_at, starting_edited_at)

    def test_update_post_requires_ownership(self):
        """Test that owning a post is required to update it"""
        new_user = sample_user(email='newuser@marsimon.com')
        new_post = Post.objects.create(author=new_user.profile, message='Post from another user', topic=self.topic)

        url = get_post_url(self.board, self.topic, new_post)
        payload = {
            'message': 'Modified post message'
        }
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        new_post.refresh_from_db()
        self.assertNotEqual(new_post.message, payload['message'])
