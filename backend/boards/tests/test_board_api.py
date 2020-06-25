from django.urls import reverse
from django.test.client import RequestFactory

from rest_framework import status

from core.extensions.test import sample_topic, sample_user, sample_board, APITestCase
from boards.models import Board
from boards.serializers import BoardSerializer


BOARDS_URL = reverse('boards:board-list')


def detail_board_url(board: Board) -> str:
    """Return the details url for a board"""
    return reverse('boards:board-detail', args=(board.id,))


class PublicBoardApiTests(APITestCase):
    """Tests for the publicly available board api"""

    def setUp(self):
        self.user = sample_user()

    def test_retrieve_board_list(self):
        """Test retrieving a list of board"""
        board = sample_board(title='Test board', description='Test board description')
        sample_topic(self.user.profile, board)
        sample_board(title='Another test board', description='Another test board description')

        res = self.client.get(BOARDS_URL)

        boards = Board.objects.all().order_by('id')
        serializer = BoardSerializer(boards, many=True, context={'request': RequestFactory().get(BOARDS_URL)})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)
        self.assertAllIn(('id', 'title', 'description', 'topics', 'created_at'), res.data[0].keys())
        self.assertAllIn(('href', 'title'), res.data[0]['topics'][0].keys())

    def test_retrieve_board_details(self):
        """Test retrieving a board's details"""
        board = sample_board()
        topic = sample_topic(self.user.profile, board)
        url = detail_board_url(board)

        res = self.client.get(url)

        serializer = BoardSerializer(board, context={'request': RequestFactory().get(url)})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.data['topics'][0]['title'], topic.title)
        self.assertAllIn(('id', 'title', 'description', 'topics', 'created_at'), res.data.keys())

    def test_create_board(self):
        """Test creating a board"""
        superuser = sample_user(superuser=True, email='super@marsimon.com')
        self.client.force_authenticate(superuser)
        payload = {
            'title': 'New board',
            'description': 'New board description'
        }
        res = self.client.post(BOARDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertAllIn(('id', 'title', 'description', 'topics', 'created_at'), res.data.keys())

        board = Board.objects.get(id=res.data['id'])
        self.assertDictMatchesAttrs(payload, board)

    def test_create_board_fails_for_basic_user(self):
        """Test that creating a board fails if not a superuser"""
        self.client.force_authenticate(self.user)
        payload = {
            'title': 'New board',
            'description': 'New board description'
        }
        res = self.client.post(BOARDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_updating_board(self):
        """Test updating a board"""
        board = sample_board(description='Old description')
        superuser = sample_user(superuser=True, email='super@marsimon.com')
        self.client.force_authenticate(superuser)

        payload = {
            'description': 'New description'
        }

        res = self.client.patch(detail_board_url(board), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        board.refresh_from_db()
        self.assertEqual(board.description, payload['description'])

    def test_update_board_fails_for_basic_user(self):
        """Test that basic users cannot update a board"""
        old_description = 'Old desciption'
        board = sample_board(description=old_description)
        self.client.force_authenticate(self.user)

        payload = {
            'description': 'New description'
        }

        res = self.client.patch(detail_board_url(board), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        board.refresh_from_db()
        self.assertEqual(board.description, old_description)
