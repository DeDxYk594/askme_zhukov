from django.urls import path, include
import django.contrib.admin
from django.conf.urls.static import static
from . import settings

import app.urls


urlpatterns = [
    path("", include(app.urls)),
    path("admin/", django.contrib.admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
