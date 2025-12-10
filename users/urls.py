from rest_framework.routers import SimpleRouter

from users.views import UserRoleViewSet

router = SimpleRouter()
router.register(r'users', UserRoleViewSet, basename='user')

urlpatterns = router.urls
