from rest_framework.reverse import reverse
from rest_framework import serializers

from boards.models import Board, Topic


class TopicWithHyperLinkSerializer(serializers.ModelSerializer):
    """Serializer with link and name for the Topic object (READ ONLY)"""
    href = serializers.SerializerMethodField()

    def get_href(self, obj: Topic):
        """Return url for current object"""
        request = self.context['request']
        return reverse('boards:boards-topic-detail', request=request, kwargs={
            'parent_lookup_board': obj.board_id,
            'pk': obj.id
        })

    class Meta:
        model = Topic
        fields = ('href', 'title')
        read_only_fields = ('href', 'title')


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for the board model"""
    topics = TopicWithHyperLinkSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'description', 'created_at', 'topics')
        read_only_fields = ('id', 'topics', 'created_at')


class TopicSerializer(serializers.ModelSerializer):
    """Serializer with link and name for the Topic object (READ ONLY)"""
    href = serializers.SerializerMethodField()

    def get_href(self, obj: Topic):
        """Return url for current object"""
        request = self.context['request']
        return reverse('boards:boards-topic-detail', request=request, kwargs={
            'parent_lookup_board': obj.board_id,
            'pk': obj.id
        })

    class Meta:
        model = Topic
        fields = ('href', 'title')
        read_only_fields = ('href', 'title')
