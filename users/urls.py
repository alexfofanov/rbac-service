from rest_framework.routers import SimpleRouter

from users.views import UserRoleViewSet

app_name = 'users'

router = SimpleRouter()
router.register(r'users', UserRoleViewSet, basename='user-role')

urlpatterns = router.urls
