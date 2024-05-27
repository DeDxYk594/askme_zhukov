from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hot", views.hot, name="hot"),
    path("question/<int:question_id>", views.question, name="question"),
    path("tag/<str:tag_id>", views.tag, name="tag"),
    path("settings", views.settings, name="settings"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("ask", views.ask, name="ask"),
    path("logout", views.logout_view, name="logout"),
    path("all_tags", views.get_all_tags),
]
