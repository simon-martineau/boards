from django.db import models
from django.utils import timezone


class Board(models.Model):
    """Model representing a board that holds topics"""
    title = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Topic(models.Model):
    """Model representing a topic that holds posts"""
    starter = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, related_name='topics', null=True)
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='topics')

    title = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    """Model representing a post made by a user"""
    author = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, related_name='posts', null=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='posts')

    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.message[:20]

    def edit_message(self, new_message: str) -> None:
        """Sets a new message and updates the edited_at field accordingly"""
        self.message = new_message
        self.edited_at = timezone.now()
        self.save(update_fields=['message', 'edited_at'])
