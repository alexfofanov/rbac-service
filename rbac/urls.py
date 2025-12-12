from rest_framework.routers import DefaultRouter

from rbac.views import BusinessElementViewSet, PermissionRuleViewSet, RoleViewSet

app_name = 'rbac'

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'elements', BusinessElementViewSet, basename='elements')
router.register(r'permission-rule', PermissionRuleViewSet, basename='permission-rule')

urlpatterns = router.urls
