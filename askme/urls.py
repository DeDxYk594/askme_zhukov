from django.urls import path, include

import app.urls


urlpatterns = [
    path("", include(app.urls)),
]
