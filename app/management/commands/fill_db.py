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
import django.contrib.auth
from tqdm import tqdm
from faker import Faker
import random


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def chunks(lst, n):
    return list(_chunks(lst, 1000))


def flatten(xss):
    return [x for xs in xss for x in xs]


class Command(BaseCommand):
    help = """Ahoy matey! This crank should give your database some fake data.
There is only one argument of this command - ratio
If ratio > 50, command will create:
- New users: ratio;
- New questions: ratio * 10;
- New answers: ratio * 100;
- New tags - ratio;
- Votes from newly created users - ratio * 200
-- Votes for users - ratio*20
-- Votes for questions: min(ratio*100, 10*ratio^2)
-- Votes for answers - the rest

If ratio <= 50, there can be less freakin data created
"""

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"]
        faker_buddy = Faker()
        print(f"You say that ratio is {ratio}")
        print("Start generate those django users...")
        django_users = [
            django.contrib.auth.models.User(
                email=faker_buddy.email(), username=faker_buddy.user_name()+faker_buddy.user_name() + str(_)
            )
            for _ in tqdm(range(ratio))
        ]
        print("Start load those django users in database...")
        for chunk in tqdm(chunks(django_users, 2)):
            django.contrib.auth.models.User.objects.bulk_create(chunk)

        print("Start generate those users (not django, but our users)...")
        users = [
            User(django_user=django_user, avatar_path=f"{random.randrange(20)}.jpg")
            for django_user in tqdm(django_users)
        ]

        print("Start load those our users in database...")
        for chunk in tqdm(chunks(users, 2)):
            User.objects.bulk_create(chunk)

        print("Start generate those tags (not django, but our users)...")
        tags_per_post = 3
        tags = [
            Tag(slug=faker_buddy.user_name()+faker_buddy.user_name()+faker_buddy.user_name(), title=faker_buddy.name())
            for ____ in tqdm(range(ratio))
        ]

        print("Start load those our tags in database...")
        for chunk in tqdm(chunks(tags, 2)):
            Tag.objects.bulk_create(chunk)

        print("Start generate those questions from our users")
        questions = [
            Question(
                user_author=random.choice(users),
                title=" ".join([faker_buddy.name() for _ in range(5)]) + "?",
                text=faker_buddy.text(),
                image_path=random.choice(
                    [
                        "lathe.png",
                        "good.jpg",
                        "lada.png",
                        "putin.jpg",
                        "schlucker.jpg",
                        "president.jpg",
                        "skala.jpg",
                        "stress.jpg",
                        "metlin.jpg",
                        "fire.jpg",
                    ]
                ),
            )
            for __ in tqdm(range(10 * ratio))
        ]

        print("Start load those questions in database...")
        for chunk in tqdm(chunks(questions, 2)):
            Question.objects.bulk_create(chunk)

        print("Start adding tags to those questions...")
        for question in tqdm(questions):
            question.tags.set(random.sample(tags, k=tags_per_post))

        print("Start generate all those answers...")
        answers = [
            Answer(
                question_to=random.choice(questions),
                user_author=random.choice(users),
                text=faker_buddy.text(),
            )
            for __ in tqdm(range(100 * ratio))
        ]

        print("Start load all those answers in our database...")
        for chunk in tqdm(chunks(answers, 2)):
            Answer.objects.bulk_create(chunk)

        print("Start generating all those likes from user to user")
        votes_to_user = [
            VoteToUser(user_from=uFrom, user_to=uTo, is_like=random.randrange(2))
            for uFrom in users
            for uTo in random.sample(users, 10)
        ]

        print("Start load all those user likes in our database...")
        for chunk in tqdm(chunks(votes_to_user, 2)):
            VoteToUser.objects.bulk_create(chunk)

        print("Start generating all those likes from user to question")
        votes_to_question = [
            VoteToQuestion(
                user_from=uFrom, question_to=qTo, is_like=random.randrange(2)
            )
            for uFrom in users
            for qTo in random.sample(questions, 10)
        ]

        print("Start load all those question likes in our database...")
        for chunk in tqdm(chunks(votes_to_question, 2)):
            VoteToQuestion.objects.bulk_create(chunk)

        print("Start generating all those likes from user to answer")
        votes_to_answer = [
            VoteToAnswer(user_from=uFrom, answer_to=aTo, is_like=random.randrange(2))
            for uFrom in users
            for aTo in random.sample(answers, 200)
        ]

        print("Start load all those answer likes in our database...")
        for chunk in tqdm(chunks(votes_to_answer, 2)):
            VoteToAnswer.objects.bulk_create(chunk)
