from typing import Any
from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from math import ceil
from .models import Question, Answer, User, Tag

from . import mock

common = {"popular_tags": mock.POPULAR_TAGS, "best_members": mock.BEST_MEMBERS}


def paginate(data, request: HttpRequest, dataPerPage: int = 5) -> tuple[list, dict]:
    """Пагинация. Начальная страница - 1"""
    try:
        currentPage = abs(int(request.GET.get("page")))
    except Exception:
        currentPage = 1
    pg = Paginator(data, dataPerPage)

    if currentPage > pg.num_pages:
        currentPage = pg.num_pages
    pagPrev = 3
    pagData = []
    if currentPage > pagPrev + 1:
        pagData.append({"pageNum": 1, "text": "1"})
        pagData.append({"pageNum": 0, "text": "..."})
        pagPrev -= 1
    for i in range(currentPage - pagPrev, currentPage):
        if i > 0:
            pagData.append({"pageNum": i, "text": f"{i}"})
    pagData.append({"pageNum": currentPage, "text": f"{currentPage}"})
    pagPost = 3
    for i in range(currentPage + 1, currentPage + 1 + pagPost):
        if i <= pg.num_pages:
            pagData.append({"pageNum": i, "text": f"{i}"})
    if pg.num_pages - currentPage > pagPost:
        pagData[-1]["pageNum"] = pg.num_pages
        pagData[-1]["text"] = str(pg.num_pages)
        pagData.insert(-1, {"pageNum": 0, "text": "..."})
    return (
        pg.get_page(currentPage),
        {"currentPage": currentPage, "paginationLinks": pagData},
    )


# class IndexView(AskmeView):
#     template_name = "index.html"


def index(request):
    questions, pagination = paginate(Question.objects.news(), request, 10)

    context = {
        "questions": questions,
        "pagination": pagination,
        "title": "New Questions",
        "hot": False,
    }

    return render(request, "index.html", context)


# class HotView(AskmeView):
#     template_name = "index.html"

# TODO


def hot(request):
    questions, pagination = paginate(Question.objects.hots(), request, 10)
    context = {
        "questions": questions,
        "pagination": pagination,
        "title": "Hot Questions",
        "hot": True,
    }
    return render(request, "index.html", context)


# class TagView(AskmeView):
#     template_name = "index.html"


def tag(request, tag_id):
    qs = Question.objects.by_tag(tag_id)
    tag=Tag.objects.get(slug=tag_id)
    questions, pagination = paginate(qs, request, 5)

    context = {
        "questions": questions,
        "pagination": pagination,
        "title": f"Search by tag: {tag.title}",
        "hot": False,
        "search": True,
    }

    return render(request, "index.html", context)


# class QuestionView(AskmeView):
#     template_name = "question.html"


def question(request, question_id):
    try:
        q = Question.objects.get(pk=question_id)
    except ZeroDivisionError:
        raise Http404()
    answers = Answer.objects.answers_for_question(q)
    page_obj, pagination = paginate(answers, request, 5)
    context = {
        "question": q,
        "answers": page_obj,
        "pagination": pagination,
        "question_id": int(question_id),
    }
    return render(request, "question.html", context)


def settings(request):
    return render(request, "settings.html")


def register(request):
    template_name = "register.html"


def login(request):
    template_name = "login.html"


def ask(request):
    template_name = "ask.html"
