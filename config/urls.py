from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='API with celery',
        default_version='v1',
        description='API'
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('', include('main.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
