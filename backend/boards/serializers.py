from rest_framework import serializers

from core.extensions.serializers import DynamicFieldsModelSerializer

from boards.models import Board, Topic


class TopicDynamicSerializer(DynamicFieldsModelSerializer):
    """Base serializer for the Topic object"""

    class Meta:
        model = Topic
        fields = '__all__'
        read_only_fields = ('id', 'starter', 'board', 'created_at')


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for the board model"""
    topics = TopicDynamicSerializer(many=True, read_only=True, fields=('id', 'title'))

    class Meta:
        model = Board
        fields = ('id', 'title', 'description', 'created_at', 'topics')
        read_only_fields = ('id', 'topics', 'created_at')

        # fields = ('id', 'title', 'description', 'topics', 'created_at')
