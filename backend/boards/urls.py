from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework.routers import DefaultRouter

from boards.views import BoardViewSet


app_name = 'boards'

router = ExtendedSimpleRouter()
router.register(r'boards', BoardViewSet, basename='board')

urlpatterns = router.urls
