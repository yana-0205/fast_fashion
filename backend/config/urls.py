from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from designs.views import health

urlpatterns = [
    path("api/health/", health),
    path("api/", include("designs.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
