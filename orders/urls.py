from rest_framework.routers import SimpleRouter

from .views import MockOrderViewSet

router = SimpleRouter()
router.register(r'orders', MockOrderViewSet, basename='order')

urlpatterns = router.urls
