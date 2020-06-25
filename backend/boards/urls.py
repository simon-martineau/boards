from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework.routers import DefaultRouter

from boards.views import BoardViewSet, TopicViewSet, PostViewSet


app_name = 'boards'

router = ExtendedSimpleRouter()
(
    router.register(r'boards', BoardViewSet, basename='board')
          .register(r'topics', TopicViewSet, basename='boards-topic', parents_query_lookups=['board'])
          .register(r'posts', PostViewSet, basename='boards-topics-post', parents_query_lookups=['topic__board', 'topic'])
)
urlpatterns = router.urls
