from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework.routers import DefaultRouter

from boards.views import BoardViewSet, TopicViewSet


app_name = 'boards'

router = ExtendedSimpleRouter()
(
    router.register(r'boards', BoardViewSet, basename='board')
          .register(r'topics', TopicViewSet, basename='boards-topic', parents_query_lookups=['board'])
)
urlpatterns = router.urls
