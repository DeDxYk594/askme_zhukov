from typing import Any
from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from math import ceil
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, User, Tag
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from .forms import LoginForm
from django.forms.models import model_to_dict
import json


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


def index(request):
    questions, pagination = paginate(Question.objects.news(), request, 10)

    context = {
        "questions": questions,
        "pagination": pagination,
        "title": "New Questions",
        "hot": False,
    }

    return render(request, "index.html", context)


def hot(request):
    questions, pagination = paginate(Question.objects.hots(), request, 10)
    context = {
        "questions": questions,
        "pagination": pagination,
        "title": "Hot Questions",
        "hot": True,
    }
    return render(request, "index.html", context)


def tag(request, tag_id):
    qs = Question.objects.by_tag(tag_id)
    tag = Tag.objects.get(slug=tag_id)
    questions, pagination = paginate(qs, request, 5)

    context = {
        "questions": questions,
        "pagination": pagination,
        "title": f"Search by tag: {tag.title}",
        "hot": False,
        "search": True,
    }

    return render(request, "index.html", context)


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
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("/")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", context={"form": form})


def logout_view(request):
    logout(request)
    if request.GET.get("next"):
        return redirect(request.GET.get("next"))
    return redirect("/")


@login_required(login_url="/login")
def ask(request):
    print(request.user.username)
    return render(request, "ask.html")


def get_all_tags(request):
    tags = [i for i in Tag.objects.all()]
    ret = [model_to_dict(i) for i in tags]
    return HttpResponse(json.dumps(ret), content_type="application/json")
