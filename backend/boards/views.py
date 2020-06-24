from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from boards.models import Board, Topic, Post
from boards.serializers import BoardSerializer, TopicWithHyperLinkSerializer

from core.permissions import ReadOnlyUnlessSuperuser


class BoardViewSet(NestedViewSetMixin, ModelViewSet):
    """Viewset for the boards model. Contains nested topics"""
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (ReadOnlyUnlessSuperuser,)


class TopicViewSet(NestedViewSetMixin, ModelViewSet):
    """Viewset for the topic model"""
    queryset = Topic.objects.all()
    serializer_class = TopicWithHyperLinkSerializer
