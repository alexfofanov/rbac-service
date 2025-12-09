from rest_framework.routers import DefaultRouter

from rbac.views import BusinessElementViewSet, PermissionRuleViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='rbac-roles')
router.register(r'elements', BusinessElementViewSet, basename='rbac-elements')
router.register(r'permission-rule', PermissionRuleViewSet, basename='permission-rule')
