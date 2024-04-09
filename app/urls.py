from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("hot", views.HotView.as_view(), name="hot"),
    path("question/<int:question_id>", views.QuestionView.as_view(), name="question"),
    path("tag/<str:tag_id>", views.TagView.as_view(), name="tag"),
    path("settings", views.SettingsView.as_view(), name="settings"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("ask", views.AskView.as_view(), name="ask"),
]
