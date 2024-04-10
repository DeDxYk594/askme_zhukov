from django.urls import path, include
import django.contrib.admin

import app.urls


urlpatterns = [
    path("", include(app.urls)),
    path("admin/", django.contrib.admin.site.urls),
]
