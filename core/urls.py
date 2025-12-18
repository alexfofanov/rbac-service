from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/rbac/', include('rbac.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('users.urls')),
]

# schema_view = get_schema_view(
#     openapi.Info(
#         title='RBAC API',
#         default_version='v1',
#         description='Описание API',
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
]
