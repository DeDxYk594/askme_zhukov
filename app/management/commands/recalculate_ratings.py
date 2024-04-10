import dis
import django.contrib.auth.models
from django.core.management.base import BaseCommand
from app.models import (
    Question,
    Answer,
    Tag,
    User,
    VoteToAnswer,
    VoteToQuestion,
    VoteToUser,
)
from django.db.models import Count, Case, When, IntegerField
import django.contrib.auth
from tqdm import tqdm
from faker import Faker
import random


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def chunks(lst, n):
    return list(_chunks(lst, n))


def flatten(xss):
    return [x for xs in xss for x in xs]


class Command(BaseCommand):
    help = """This crank should give rating attributes of your tables some refresh!"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Recalculating user ratings...")
        users_with_like_count = User.objects.annotate(
            likes_count=Count(
                Case(
                    When(user_to_who_is_vote__is_like=True, then=1),
                    output_field=IntegerField(),
                )
            ),
            dislikes_count=Count(
                Case(
                    When(user_to_who_is_vote__is_like=False, then=1),
                    output_field=IntegerField(),
                )
            ),
        )

        for user in tqdm(users_with_like_count):
            User.objects.filter(id=user.id).update(
                rating_likes=user.likes_count, rating_dislikes=user.dislikes_count
            )

        print("Recalculating questions ratings...")
        questions_with_like_count = Question.objects.annotate(
            likes_count=Count(
                Case(
                    When(votetoquestion__is_like=True, then=1),
                    output_field=IntegerField(),
                )
            ),
            dislikes_count=Count(
                Case(
                    When(votetoquestion__is_like=False, then=1),
                    output_field=IntegerField(),
                )
            ),
        )

        for question in tqdm(questions_with_like_count):
            Question.objects.filter(id=user.id).update(
                rating_likes=question.likes_count,
                rating_dislikes=question.dislikes_count,
            )

        print("Recalculating answer ratings...")
        answers_with_like_count = Answer.objects.annotate(
            likes_count=Count(
                Case(
                    When(votetoanswer__is_like=True, then=1),
                    output_field=IntegerField(),
                )
            ),
            dislikes_count=Count(
                Case(
                    When(votetoanswer__is_like=False, then=1),
                    output_field=IntegerField(),
                )
            ),
        )

        for answer in tqdm(answers_with_like_count):
            Answer.objects.filter(id=user.id).update(
                rating_likes=answer.likes_count, rating_dislikes=answer.dislikes_count
            )
