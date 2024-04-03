from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hot", views.hot, name="hot"),
    path("question/<int:question_id>", views.question, name="question"),
    path("tag/<str:tag_id>", views.tag, name="tag"),
    path("settings", views.settings, name="settings"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("ask", views.ask, name="ask"),
]
