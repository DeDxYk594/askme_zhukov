from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from math import ceil
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, User, Tag
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from .forms import LoginForm, AskForm, AnswerForm, RegisterForm, SettingsForm
from django.forms.models import model_to_dict
import json
import django.contrib.auth.models


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


def question(request: HttpRequest, question_id):
    try:
        q = Question.objects.get(pk=question_id)
    except ZeroDivisionError:
        raise Http404()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data["answer"]
            if len(answer_text) != 0:
                ans = Answer(
                    question_to=q,
                    text=answer_text,
                    user_author=User.objects.get(django_user=request.user),
                )
                ans.save()
                return redirect("question", question_id=question_id)

    answers = Answer.objects.answers_for_question(q, user=request.user)
    page_obj, pagination = paginate(answers, request, 5)
    context = {
        "question": q,
        "answers": page_obj,
        "pagination": pagination,
        "question_id": int(question_id),
    }
    return render(request, "question.html", context)


@login_required(login_url="/login")
def settings(request: HttpRequest):
    askme_user = User.objects.get(django_user=request.user)
    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES)
        form.is_valid()
        if form.cleaned_data.get("password"):
            if form.cleaned_data.get("password") and form.cleaned_data.get(
                "repeat_password"
            ):
                if form.cleaned_data.get("password") != form.cleaned_data.get(
                    "repeat_password"
                ):
                    form.add_error("repeat_password", "Passwords dont match")
            else:
                form.add_error("repeat_password", "Should input password twice")
        else:
            if form.cleaned_data.get("repeat_password"):
                form.add_error("password", "Should input password twice")

        if (
            form.cleaned_data.get("username")
            and form.cleaned_data.get("username") != request.user.username
        ):
            if django.contrib.auth.models.User.objects.filter(
                username=form.cleaned_data["username"]
            ).count():
                form.add_error("username", "This username is already used")
        if (
            form.cleaned_data.get("email")
            and form.cleaned_data.get("email") != request.user.email
        ):
            if django.contrib.auth.models.User.objects.filter(
                email=form.cleaned_data["email"]
            ).count():
                form.add_error("email", "This email is already used")
        if(form.is_valid()):
            request.user.username=form.cleaned_data.get("username")
            request.user.email=form.cleaned_data.get("email")
            if(form.cleaned_data.get("password")):
                request.user.set_password(form.cleaned_data.get("password"))
            request.user.save()
            if(form.cleaned_data.get("avatar")):
                askme_user.avatar=form.cleaned_data.get("avatar")
                askme_user.save()
            return render(request, "settings.html", {"askme_user": askme_user,"settings_success":True})
        return render(request, "settings.html", {"askme_user": askme_user,"form":form})


    else:
        return render(request, "settings.html", {"askme_user": askme_user})


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        form.is_valid()
        if form.cleaned_data.get("username"):
            if django.contrib.auth.models.User.objects.filter(
                username=form.cleaned_data["username"]
            ).count():
                form.add_error("username", "This username is already used")
        if form.cleaned_data.get("email"):
            if django.contrib.auth.models.User.objects.filter(
                email=form.cleaned_data["email"]
            ).count():
                form.add_error("email", "This email is already used")
        if form.cleaned_data.get("password") and form.cleaned_data.get(
            "repeat_password"
        ):
            if form.cleaned_data["password"] != form.cleaned_data["repeat_password"]:
                form.add_error("repeat_password", "Passwords not match")
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            newDjangoUser = django.contrib.auth.models.User(
                username=username,
                email=email,
                password=password,
            )
            newDjangoUser.save()
            newUser = User(
                django_user=newDjangoUser, avatar=form.cleaned_data["avatar"]
            )
            newUser.save()
            login(request, newDjangoUser)
            return redirect("index")

        return render(request, "register.html", context={"form": form})
    else:
        return render(request, "register.html")


def login_view(request: HttpRequest):
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


def logout_view(request: HttpRequest):
    logout(request)
    if request.GET.get("next"):
        return redirect(request.GET.get("next"))
    return redirect("/")


@login_required(login_url="/login")
def ask(request: HttpRequest):
    if request.method == "POST":
        form = AskForm(request.POST, request.FILES)
        form.is_valid()
        tags = Tag.objects.resolve_from_form(form)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            image = form.cleaned_data["image"]
            askme_user = User.objects.get(django_user=request.user)
            newQuestion = Question(
                user_author=askme_user, title=title, text=text, image=image
            )
            newQuestion.save()
            newQuestion.tags.set(tags)
            return redirect("question", newQuestion.pk)
        return render(
            request, "ask.html", context={"all_tags": Tag.objects.all(), "form": form}
        )
    else:
        return render(request, "ask.html", context={"all_tags": Tag.objects.all()})
