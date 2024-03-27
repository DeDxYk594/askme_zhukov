from django.urls import path

from . import views

urlpatterns = [
    path("",views.index),
    path("hot.html",views.hot),
    path("questions/<int:question_id>",views.question,name="question"),
]
