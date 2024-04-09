from typing import Any
from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from math import ceil

from . import mock

common = {"popular_tags": mock.POPULAR_TAGS, "best_members": mock.BEST_MEMBERS}


class AskmeView(TemplateView):
    def get_context_data(self, **kwargs) -> dict:
        context = {"popular_tags": mock.POPULAR_TAGS, "best_members": mock.BEST_MEMBERS}
        return context


def paginate(data, pageNumber: int, dataPerPage: int = 5) -> tuple[list, list]:
    """Пагинация. Начальная страница - 1"""
    pg = Paginator(data, dataPerPage)
    pagPrev = 3
    pagData = []
    if pageNumber > pagPrev + 1:
        pagData.append({"pageNum": 1, "text": "1"})
        pagData.append({"pageNum": 0, "text": "..."})
        pagPrev -= 1
    for i in range(pageNumber - pagPrev, pageNumber):
        if i > 0:
            pagData.append({"pageNum": i, "text": f"{i}"})
    pagData.append({"pageNum": pageNumber, "text": f"{pageNumber}"})
    pagPost = 3
    for i in range(pageNumber + 1, pageNumber + 1 + pagPost):
        if i <= pg.num_pages:
            pagData.append({"pageNum": i, "text": f"{i}"})
    if pg.num_pages - pageNumber > pagPost:
        pagData[-1]["pageNum"] = pg.num_pages
        pagData[-1]["text"] = str(pg.num_pages)
        pagData.insert(-1, {"pageNum": 0, "text": "..."})
    return (pg.get_page(pageNumber), pagData)


class IndexView(AskmeView):
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except Exception:
            page_num = 1
        questions, pagination = paginate(mock.QUESTIONS, page_num, 1)

        for q in questions:
            for a in q["answers"]:
                a["user"] = mock.USERS[a["user_id"]]
        context.update(
            {
                "questions": questions,
                "pagination": pagination,
                "current_page": page_num,
                "title": "New Questions",
                "hot": False,
            }
        )
        return context


class HotView(AskmeView):
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_num = int(self.request.GET.get("page", 1))
        questions, pagination = paginate(mock.QUESTIONS, page_num, 5)

        for q in questions:
            for a in q["answers"]:
                a["user"] = mock.USERS[a["user_id"]]
        context.update(
            {
                "questions": list(reversed(questions)),
                "pagination": pagination,
                "current_page": page_num,
                "title": "New Questions",
                "hot": True,
            }
        )
        return context


class TagView(AskmeView):
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_num = int(self.request.GET.get("page", 1))
        try:
            tag_id = self.kwargs["tag_id"]
        except Exception:
            raise Http404

        qs = [q for q in mock.QUESTIONS if tag_id in q["tags"]]
        questions, pagination = paginate(qs, page_num, 5)

        for q in questions:
            for a in q["answers"]:
                a["user"] = mock.USERS[a["user_id"]]
        context.update(
            {
                "questions": list(reversed(questions)),
                "pagination": pagination,
                "current_page": page_num,
                "title": f"Search: tag={tag_id}",
                "hot": False,
                "search": True,
            }
        )
        return context


class QuestionView(AskmeView):
    template_name = "question.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        question_id = self.kwargs["question_id"]
        context = super().get_context_data(**kwargs)
        q = mock.QUESTIONS[question_id - 1]
        for a in q["answers"]:
            a["user"] = mock.USERS[a["user_id"]]
        context.update({"question": q})
        return context


class SettingsView(AskmeView):
    template_name = "settings.html"


class RegisterView(AskmeView):
    template_name = "register.html"


class LoginView(AskmeView):
    template_name = "login.html"


class AskView(AskmeView):
    template_name = "ask.html"
