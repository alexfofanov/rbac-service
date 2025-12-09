from django.contrib import admin
from django.urls import include, path

from rbac.urls import router as rbac_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/rbac/', include(rbac_router.urls)),
]
