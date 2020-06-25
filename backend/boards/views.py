from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from boards.models import Board, Topic, Post
from boards.serializers import BoardSerializer, TopicSerializer, CreateTopicSerializer, TopicListSerializer

from core.permissions import ReadOnlyUnlessSuperuser, TopicPermission


class BoardViewSet(NestedViewSetMixin, ModelViewSet):
    """Viewset for the boards model. Contains nested topics"""
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (ReadOnlyUnlessSuperuser,)


class TopicViewSet(NestedViewSetMixin, ModelViewSet):
    """Viewset for the topic model"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (TopicPermission,)

    def list(self, request, *args, **kwargs):
        self.serializer_class = TopicListSerializer
        return super(TopicViewSet, self).list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(board_id=self.kwargs['parent_lookup_board'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTopicSerializer
        return self.serializer_class
