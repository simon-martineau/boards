from rest_framework import serializers

from boards.models import Board, Topic


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for the topic model"""
    class Meta:
        model = Topic
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for the board model"""
    topics = TopicSerializer(many=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'description', 'topics', 'created_at')
