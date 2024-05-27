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
from app.utils import chunks, recalculateRating, slugify

with open("app/management/commands/allicons.txt") as f:
    ALL_ICONS = [i.strip().replace("\x00", "") for i in f.readlines()]
ALL_ICONS = [i for i in ALL_ICONS if len(i) > 3]

with open("app/management/commands/allcolors.txt") as f:
    ALL_COLORS = [i.strip().replace("\x00", "") for i in f.readlines()]
ALL_COLORS = [i for i in ALL_COLORS if len(i) > 3]


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
                email=faker_buddy.email(),
                username=faker_buddy.user_name() + faker_buddy.user_name() + str(_),
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
        for chunk in tqdm(chunks(users)):
            User.objects.bulk_create(chunk)
        print("Start generate tag names (not models yet)")
        tag_titles = list(
            set([faker_buddy.word().capitalize() for _ in tqdm(range(ratio * 10))])
        )[:ratio]
        tag_slugs = [slugify(tag) for tag in tag_titles]
        print("Start generate those tags ...")
        tags_per_post = 3
        tags = [
            Tag(
                slug=slug,
                title=title,
                bootstrap_icon=random.choice(ALL_ICONS),
                color=random.choice(ALL_COLORS),
            )
            for (title, slug) in tqdm(zip(tag_titles, tag_slugs))
        ]

        print("Start load those our tags in database...")
        for chunk in tqdm(chunks(tags, n=1)):
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
        for chunk in tqdm(chunks(questions)):
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
        for chunk in tqdm(chunks(answers)):
            Answer.objects.bulk_create(chunk)

        print("Start generating all those likes from user to user")
        votes_to_user = [
            VoteToUser(user_from=uFrom, user_to=uTo, is_like=random.randrange(2))
            for uFrom in tqdm(users)
            for uTo in random.sample(users, 10)
        ]

        print("Start load all those user likes in our database...")
        for chunk in tqdm(chunks(votes_to_user)):
            VoteToUser.objects.bulk_create(chunk)

        print("Start generating all those likes from user to question")
        votes_to_question = [
            VoteToQuestion(
                user_from=uFrom, question_to=qTo, is_like=random.randrange(2)
            )
            for uFrom in tqdm(users)
            for qTo in random.sample(questions, 10)
        ]

        print("Start load all those question likes in our database...")
        for chunk in tqdm(chunks(votes_to_question)):
            VoteToQuestion.objects.bulk_create(chunk)

        print("Start generating all those likes from user to answer")
        votes_to_answer = [
            VoteToAnswer(user_from=uFrom, answer_to=aTo, is_like=random.randrange(2))
            for uFrom in tqdm(users)
            for aTo in random.sample(answers, 200)
        ]

        print("Start load all those answer likes in our database...")
        for chunk in tqdm(chunks(votes_to_answer)):
            VoteToAnswer.objects.bulk_create(chunk)

        print("We need to recalculate denormalization for our db, so wait SO MORE")
        recalculateRating()
