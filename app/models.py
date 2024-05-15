from django.db import models
import django.contrib.auth.models

from app.mock import QUESTIONS


class TagManager(models.Manager):
    def normalized_rating(self):
        """Вычислить нормализованный рейтинг"""
        return self.annotate(question_count=models.Count("question"))

    def tops(self):
        return self.order_by("-rating_questions")


class UserManager(models.Manager):
    def normalized_rating(self):
        """Вычислить нормализованный рейтинг"""
        return self.annotate(
            likes_count=models.Count(
                models.Case(
                    models.When(user_to_who_is_vote__is_like=True, then=1),
                    output_field=models.IntegerField(),
                )
            ),
            dislikes_count=models.Count(
                models.Case(
                    models.When(user_to_who_is_vote__is_like=False, then=1),
                    output_field=models.IntegerField(),
                )
            ),
            questions_count=models.Count("question"),
            answers_count=models.Count("answer"),
        )

    def bests(self):
        """Вычислить рейтинг пользователя по формуле и отсортировать пользователей по убыванию рейтинга"""
        return self.annotate(
            rating_points=models.ExpressionWrapper(
                models.F("rating_likes") * 100
                - models.F("rating_dislikes") * 200
                + models.F("rating_answers") * 10,
                output_field=models.BigIntegerField(),
            )
        ).order_by("-rating_points")


# Добавить запрос на получение самых новых, самых популярных, сделать вопросы по тегу
class QuestionManager(models.Manager):
    def normalized_rating(self):
        """Вычислить нормализованный рейтинг"""
        return self.annotate(
            answers_count=models.Count("answer"),
        ).annotate(
            likes_count=models.Count(
                models.Case(
                    models.When(votetoquestion__is_like=True, then=1),
                    output_field=models.IntegerField(),
                )
            ),
            dislikes_count=models.Count(
                models.Case(
                    models.When(votetoquestion__is_like=False, then=1),
                    output_field=models.IntegerField(),
                )
            ),
        )

    def news(self):
        return self.order_by("-created_at")

    def hots(self):
        return self.annotate(
            rating_points=models.ExpressionWrapper(
                models.F("rating_likes") * 10
                - models.F("rating_dislikes") * 20
                + models.F("rating_answers") * 15,
                output_field=models.BigIntegerField(),
            )
        ).order_by("-rating_points")

    def by_tag(self, tag_id: str):
        return self.filter(tags__slug=tag_id)


class AnswerManager(models.Manager):
    def normalized_rating(self):
        """Вычислить нормализованный рейтинг"""
        return self.annotate(
            likes_count=models.Count(
                models.Case(
                    models.When(votetoanswer__is_like=True, then=1),
                    output_field=models.IntegerField(),
                )
            ),
            dislikes_count=models.Count(
                models.Case(
                    models.When(votetoanswer__is_like=False, then=1),
                    output_field=models.IntegerField(),
                )
            ),
        )

    def answers_for_question(self, question):
        return (
            self.filter(question_to=question)
            .annotate(
                rating_points=models.ExpressionWrapper(
                    models.F("rating_likes") * 100 - models.F("rating_dislikes") * 200,
                    output_field=models.BigIntegerField(),
                )
            )
            .order_by("-rating_points")
        )


class Tag(models.Model):
    objects = TagManager()
    slug = models.SlugField(max_length=200, unique=True)
    title = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating_questions = models.BigIntegerField(default=0)


class User(models.Model):
    objects = UserManager()
    django_user = models.OneToOneField(
        django.contrib.auth.models.User, on_delete=models.CASCADE
    )
    avatar_path = models.TextField(max_length=300)
    rating_likes = models.BigIntegerField(default=0)
    rating_dislikes = models.BigIntegerField(default=0)
    rating_questions = models.BigIntegerField(default=0)
    rating_answers = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.django_user.username


class Question(models.Model):
    objects = QuestionManager()
    user_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    title = models.TextField(max_length=200)
    text = models.TextField(max_length=2000)
    image_path = models.TextField(max_length=300)  # TODO Сделать ImageField
    rating_likes = models.BigIntegerField(default=0)
    rating_dislikes = models.BigIntegerField(default=0)
    rating_answers = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    objects = AnswerManager()
    question_to = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=2000)
    rating_likes = models.BigIntegerField(default=0)
    rating_dislikes = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VoteToUser(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_who_vote"
    )
    user_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_to_who_is_vote"
    )
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = [["user_from", "user_to"]]


class VoteToQuestion(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_who_vote_to_q"
    )
    question_to = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = [["user_from", "question_to"]]


class VoteToAnswer(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_who_vote_to_a"
    )
    answer_to = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = [["user_from", "answer_to"]]
