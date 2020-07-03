from django.http import HttpRequest

from rest_framework.reverse import reverse
from rest_framework import serializers

from accounts.serializers import ProfileWithHyperlinkSerializer
from boards.models import Board, Topic, Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the post object"""
    author = ProfileWithHyperlinkSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'topic', 'message', 'created_at', 'edited_at', 'author')
        read_only_fields = ('id', 'topic', 'created_at', 'edited_at', 'author')

    def update(self, instance: Post, validated_data):
        message = validated_data.pop('message')
        instance.edit_message(message)
        return super().update(instance, validated_data)

    def create(self, validated_data: dict) -> Post:
        """Takes the message field and created a starting post for a new topic"""
        request: HttpRequest = self.context['request']
        validated_data['author'] = request.user.profile

        return super().create(validated_data)


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


class TopicSerializer(serializers.ModelSerializer):
    """Detailed serializer for the topic object"""
    starter = ProfileWithHyperlinkSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'board', 'title', 'created_at', 'starter', 'posts')
        read_only_fields = ('id', 'board', 'starter', 'posts', 'created_at')


# noinspection PyMethodMayBeStatic
class TopicListSerializer(serializers.ModelSerializer):
    """Detailed serializer for the topic object"""
    starter = ProfileWithHyperlinkSerializer(read_only=True)
    first_post = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    def get_first_post(self, obj: Topic):
        return PostSerializer(obj.posts.order_by('created_at').first(), read_only=True, context=self.context).data

    def get_post_count(self, obj: Topic):
        return obj.posts.count()

    class Meta:
        model = Topic
        fields = ('id', 'board', 'title', 'post_count', 'created_at', 'starter', 'first_post')
        read_only_fields = ('id', 'board', 'post_count', 'created_at', 'starter', 'first_post')


class CreateTopicSerializer(serializers.ModelSerializer):
    """Serializer to create a topic"""
    starter = ProfileWithHyperlinkSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    message = serializers.CharField(write_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'board', 'title', 'message', 'created_at', 'starter', 'posts')
        read_only_fields = ('id', 'board', 'starter', 'posts', 'created_at')

    def create(self, validated_data: dict) -> Topic:
        """Takes the message field and created a starting post for a new topic"""
        request: HttpRequest = self.context['request']
        message = validated_data.pop('message')
        validated_data['starter'] = request.user.profile
        topic = super().create(validated_data)
        Post.objects.create(author=request.user.profile, message=message, topic=topic)

        return topic


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for the board model"""
    topics = TopicWithHyperLinkSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'description', 'created_at', 'topics')
        read_only_fields = ('id', 'topics', 'created_at')
