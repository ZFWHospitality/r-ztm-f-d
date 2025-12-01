from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework import routers
from tasks.views import TaskViewSet, UserCreateViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserCreateViewSet, basename='user')

schema_view = get_schema_view(
   openapi.Info(
      title="Task Manager API",
      default_version='v1',
      description="Task Manager API for Zippee assignment — JWT auth, CRUD for tasks",
      contact=openapi.Contact(email="you@example.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
