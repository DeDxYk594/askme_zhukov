from app.models import (
    Question,
    Answer,
    Tag,
    User,
    VoteToAnswer,
    VoteToQuestion,
    VoteToUser,
)
from django.db import models
from tqdm import tqdm
import re
import datetime
from django.core.cache import cache


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def chunks(lst, n=1000):
    return list(_chunks(lst, n))


def slugify(text):
    """Заменить в тексте пробелы на подчёркивания,"""
    text = text.lower()
    text = text.replace(" ", "_")
    text = re.sub(r"[^a-z0-9_]", "", text)
    return text


def recalculateRating():
    print("Recalculating users ratings...")

    calculated_users = User.objects.normalized_rating()
    for user in tqdm(calculated_users):
        user.rating_likes = user.likes_count
        user.rating_dislikes = user.dislikes_count
        user.rating_questions = user.questions_count
        user.rating_answers = user.answers_count

    print("Loading user rating into database..")

    for chunk in tqdm(chunks(calculated_users)):
        User.objects.bulk_update(
            chunk,
            ["rating_likes", "rating_dislikes", "rating_questions", "rating_answers"],
        )

    print("Recalculating questions ratings...")

    calculated_questions = Question.objects.normalized_rating()
    for question in tqdm(calculated_questions):
        question.rating_likes = question.likes_count
        question.rating_dislikes = question.dislikes_count
        question.rating_answers = question.answers_count

    print("Loading question rating into database..")

    for chunk in tqdm(chunks(calculated_questions)):
        Question.objects.bulk_update(
            chunk, ["rating_likes", "rating_dislikes", "rating_answers"]
        )

    print("Recalculating answers ratings...")

    calculated_answers = Answer.objects.normalized_rating()
    for answer in tqdm(calculated_answers):
        answer.rating_likes = answer.likes_count
        answer.rating_dislikes = answer.dislikes_count

    print("Loading answer rating into database..")

    for chunk in tqdm(chunks(calculated_answers)):
        Answer.objects.bulk_update(chunk, ["rating_likes", "rating_dislikes"])

    print("Recalculating tags ratings...")

    calculated_tags = Tag.objects.normalized_rating()
    for tag in tqdm(calculated_tags):
        tag.rating_questions = tag.question_count

    print("Loading tag rating into database..")

    for chunk in tqdm(chunks(calculated_tags)):
        Tag.objects.bulk_update(chunk, ["rating_questions"])


def updateTags():
    three_months_ago = datetime.datetime.now() - datetime.timedelta(days=90)
    popular_tags = (
        Tag.objects.filter(question__created_at__gte=three_months_ago)
        .annotate(num_questions=models.Count("question"))
        .order_by("-num_questions")[:10]
    )

    cache.set("popular_tags", popular_tags, 60 * 60 * 24)  # Кэшируем на сутки


def updateUsers():
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    popular_users = (
        User.objects.filter(models.Q(question__created_at__gte=last_week))
        .annotate(popularity=models.Count("question") + models.Count("answer"))
        .order_by("-popularity")[:10]
    )

    cache.set("popular_users", popular_users, 60 * 60 * 24)  # Кэшируем на сутки


def updateCache():
    updateTags()
    updateUsers()
