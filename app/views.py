from ast import Dict
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from math import ceil

from . import mock

common = {"popular_tags": mock.POPULAR_TAGS, "best_members": mock.BEST_MEMBERS}

class AskmeView(TemplateView):
    def get_context_data(self, **kwargs) -> dict:
        context = {"popular_tags": mock.POPULAR_TAGS, "best_members": mock.BEST_MEMBERS}
        context.update(self.get_page_data(**kwargs))
        return context

    def get_page_data(self, **kwargs) -> dict:
        return {}


def paginate(data: list, pageNumber: int, dataPerPage: int = 5) -> tuple[list, list]:
    """Пагинация. Начальная страница - 1.
    @returns ([...данные к отображению], [2,3,4,5,6,7,8,9])"""
    totalPages = ceil(len(data) / dataPerPage)
    retData = data[dataPerPage * (pageNumber - 1) : dataPerPage * pageNumber]
    pagPrev = 3
    pagData = []
    if pageNumber > pagPrev + 1:
        pagData.append(1)
        pagPrev -= 1
    for i in range(pageNumber - pagPrev, pageNumber):
        if i > 0:
            pagData.append(i)
    pagData.append(pageNumber)
    pagPost = 3
    for i in range(pageNumber + 1, pageNumber + 1 + pagPost):
        if i <= totalPages:
            pagData.append(i)
    if totalPages - pageNumber > pagPost + 1:
        pagData[-1] = totalPages
    print(pagData)
    return (retData, pagData)


class IndexView(AskmeView):
    template_name = "index.html"

    def get_page_data(self, **kwargs) -> dict:
        page_num = int(self.request.GET.get("page", 1))
        questions, pagination = paginate(mock.QUESTIONS, page_num, 2)

        for q in questions:
            for a in q["answers"]:
                a["user"] = mock.USERS[a["user_id"]]
        return {
            "questions": questions,
            "pagination": pagination,
            "current_page": page_num,
            "title": "New Questions",
            "hot":False,
        }


def index(request: HttpRequest) -> HttpResponse:
    page_num = int(request.GET.get("page", 1))
    questions, pagination = paginate(mock.QUESTIONS, page_num, 2)

    for q in questions:
        for a in q["answers"]:
            a["user"] = mock.USERS[a["user_id"]]
    print(questions)
    print("12345")

    return render(
        request,
        "index.html",
        dict(
            {
                "questions": questions,
                "pagination": pagination,
                "current_page": page_num,
                "title": "New Questions",
            },
            **common,
        ),
    )


def tag(request: HttpRequest, tag_id: str) -> HttpResponse:
    page_num = int(request.GET.get("page", 1))
    qs = [q for q in mock.QUESTIONS if tag_id in q["tags"]]
    questions, pagination = paginate(mock.QUESTIONS, page_num, 2)

    for q in questions:
        for a in q["answers"]:
            a["user"] = mock.USERS[a["user_id"]]
    print(questions)
    print("12345")

    return render(
        request,
        "index.html",
        dict(
            {
                "questions": questions,
                "pagination": pagination,
                "current_page": page_num,
                "title": f"Questions with tag {tag_id}",
            },
            **common,
        ),
    )


def hot(request: HttpRequest) -> HttpResponse:
    return render(request, "hot.html", {"questions": reversed(mock.QUESTIONS)})


def question(request: HttpRequest, question_id) -> HttpResponse:
    q = mock.QUESTIONS[question_id - 1]
    for a in q["answers"]:
        a["user"] = mock.USERS[a["user_id"]]
    return render(request, "question.html", dict({"question": q}, **common))


def settings(request: HttpRequest) -> HttpResponse:
    return render(request, "settings.html", dict({}, **common))


def register(request: HttpRequest) -> HttpResponse:
    return render(request, "register.html", dict({}, **common))


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html", dict({}, **common))


def ask(request: HttpRequest) -> HttpResponse:
    return render(request, "ask.html", dict({}, **common))
